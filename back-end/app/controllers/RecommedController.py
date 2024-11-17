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


class RecommendedController:
    collection_name = "Recommended"

    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

        self.client = weaviate.connect_to_local(
            host=WEAVIATE_URL,
        )

        self.embed_model = OllamaEmbedding(
            model_name=OLLAMA_EMBEDDING_MODEL,
            base_url=OLLAMA_BASE_URL,
        )

        self._create_schema(collection_name=self.collection_name)

        self._vector_store = WeaviateVectorStore(
            weaviate_client=self.client,
            index_name=self.collection_name,
            text_key="content",
            metadata_keys=["topic"],
        )
        self._storage_context = StorageContext.from_defaults(
            vector_store=self._vector_store
        )
        self._index = VectorStoreIndex.from_vector_store(
            self._vector_store,
            embed_model=self.embed_model,
        ).as_retriever()

    def _create_schema(self, collection_name):
        try:
            self.client.collections.get(self.collection_name)
        except:
            self.client.collections.create(
                name=collection_name,
                vectorizer_config={"none": {"vectorizerModule": None}},
                properties=[
                    {
                        "name": "content",
                        "dataType": ["text"],
                    },
                    {
                        "name": "topic",
                        "dataType": ["text"],
                    },
                ],
            )

    async def get_recommed(self, current_user: User):
        query_user_interest = (
            select(UserInterest)
            .where(UserInterest.user_id == current_user.user_id)
            .order_by(desc(UserInterest.updated_at), desc(UserInterest.score))
            .limit(10)
        )
        result = await self.db.execute(query_user_interest)
        result = result.scalars().all()

        product_embedding_dict = {"product_name": [], "score": []}
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
            print(product)
            product_id = product.node.metadata.get("product_id", None)
            if product_id is None:
                continue

            product_ids.append(product_id)

        product_get_query = select(Product).where(Product.product_id in product_ids)
        results = await self.db.execute(product_get_query)
        results = [ProductResponse.model_validate(pro) for pro in results.scalars()]
        return JSONResponse(content=results, status_code=status.HTTP_200_OK)

    async def get_default_recommed(self):
        pass
