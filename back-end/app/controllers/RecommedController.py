from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, status
from db_connector import get_db
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Document
from llama_index.vector_stores.weaviate import WeaviateVectorStore
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.core import StorageContext
from sqlalchemy import select, update, insert, desc
from models.UserInterest import UserInterest
from models.Users import User
from models.CategoryProduct import CategoryProduct
from models.Category import Category
from models.Products import Product
from fastapi.responses import JSONResponse
import weaviate
from serializers.ProductSerializers import ProductResponse
import weaviate.classes.query as wq
import numpy as np
from config import (
    WEAVIATE_URL,
    OLLAMA_EMBEDDING_MODEL,
    OLLAMA_BASE_URL,
)
import logging


logger = logging.getLogger(__name__)


class RecommendedController:
    collection_name = "Recommend"

    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db
        try:
            self.client = weaviate.connect_to_local(
                host=WEAVIATE_URL,
                port=8080
            )

            self.embed_model = OllamaEmbedding(
                model_name=OLLAMA_EMBEDDING_MODEL,
                base_url=OLLAMA_BASE_URL,
                request_timeout=500.0, 
                show_progress=True,
            )

            self._create_schema()

            self._vector_store = WeaviateVectorStore(
                weaviate_client=self.client,
                index_name=self.collection_name,
                text_key="content",
                metadata_keys=["topic", "product_id"],
            )
            self._storage_context = StorageContext.from_defaults(
                vector_store=self._vector_store
            )
            self._index = VectorStoreIndex.from_vector_store(
                self._vector_store,
                embed_model=self.embed_model,
            ).as_retriever()
        except Exception as e:
            if hasattr(self, 'client'):
                self.client.close()

    def _create_schema(self):
        if not self.client.is_connected():
            self.client.connect()
        try:
            self.client.collections.get(self.collection_name)
        except weaviate.exceptions.SchemaValidationException:
            self.client.collections.create_from_dict(
                {
                    "class": self.collection_name,
                    "vectorizer": None,
                    "properties": [
                        {"name": "content", "dataType": ["text"]},
                        {"name": "topic", "dataType": ["text"]},
                        {"name": "product_id", "dataType": ["text"]},
                    ],
                }
            )
        


    def __del__(self):
        if hasattr(self, 'client') and self.client is not None:
            self.client.close()


    async def get_recommed(self, current_user: User):
        try:
            self.client.connect()
            query_user_interest = (
                select(UserInterest)
                .where(UserInterest.user_id == current_user.user_id)
                .order_by(desc(UserInterest.updated_at), desc(UserInterest.score))
                .limit(10)
            )
            result = await self.db.execute(query_user_interest)
            result = result.scalars().all()

            product_embedding_dict = {"product_name": [], "score": []}

            if not result:
                return JSONResponse(content=[], status_code=status.HTTP_200_OK)

            for product in result or []:

                all_cat_names_query = select(CategoryProduct).where(
                    CategoryProduct.product_id == product.product_id
                )
                results_cat = await self.db.execute(all_cat_names_query)
                results_cat = results_cat.scalars()

                cat_names = ""
                for cat in results_cat:
                    cat_names_query = select(Category).where(Category.cat_id == cat.cat_id)
                    cat = await self.db.execute(cat_names_query)
                    cat_names += cat.scalar_one_or_none().cat_name

                product_name_query = select(Product).where(
                    Product.product_id == product.product_id
                )
                product_obj = await self.db.execute(product_name_query)
                product_obj = product_obj.scalar_one_or_none()
                product_text = f"{product_obj.product_name * 3} {cat_names * 2}"

                product_embedding_dict["product_name"].append(product_text)
                product_embedding_dict["score"].append(product.score)

            embedding_vectors = self.embed_model.get_text_embedding_batch(
                texts=product_embedding_dict["product_name"], show_progress=True
            )
            scores = np.array(product_embedding_dict["score"])
            weighted_sum = np.zeros_like(embedding_vectors[0])

            for vector, score in zip(embedding_vectors, scores):
                weighted_sum += vector * score

            average_vectors = (
                weighted_sum / np.sum(scores) if np.sum(scores) != 0 else weighted_sum
            )

            _index = self.client.collections.get(self.collection_name)
            vector_result = _index.query.near_vector(
                near_vector=average_vectors,
                limit=10,
                return_metadata=wq.MetadataQuery(score=True),
            )
            
            product_ids = []
            for product in vector_result.objects or []:
                product_id = product.properties.get("product_id", None)
                if product_id is None:
                    continue

                product_ids.append(product_id)

            product_get_query = select(Product).where(Product.product_id.in_(product_ids))
            product_results = await self.db.execute(product_get_query)
            products = []
            for pro in product_results.scalars():
                products.append({"product_id": str(pro.product_id), "product_name" : pro.product_name, "product_price" : pro.price})
           
            return JSONResponse(content=products, status_code=status.HTTP_200_OK)

        except Exception as e:
            await self.db.rollback()
            logger.error(str(e))


    async def get_default_recommed(self):
        try:
            get_product_query = select(Product).limit(256)
            products = await self.db.execute(get_product_query)
            products = products.scalars().all()
            return JSONResponse(content=products, status_code=status.HTTP_200_OK)
        except Exception as e:
            await self.db.rollback()
            logger.error(str(e))
