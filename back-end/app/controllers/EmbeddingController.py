from bs4 import BeautifulSoup
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Document
from llama_index.vector_stores.weaviate import WeaviateVectorStore
from llama_index.core import StorageContext
from llama_index.embeddings.ollama import OllamaEmbedding
import weaviate
from helper_collections.FAQQUES import FAQ
from typing import Optional, List
from models.Products import *
from config import (
    OLLAMA_CHAT_MODEL,
    OLLAMA_BASE_URL,
    WEAVIATE_URL,
    OLLAMA_EMBEDDING_MODEL,
)
from models.CategoryProduct import CategoryProduct
from models.Category import Category
from sqlalchemy import select, update, insert
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from db_connector import get_db
from serializers.ProductSerializers import ProductResponse
from fastapi import status
from fastapi.responses import JSONResponse
from loguru import logger


class EmbeddingController:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db
        self.client = weaviate.connect_to_local(
            host=WEAVIATE_URL,
        )

        self.embed_model = OllamaEmbedding(
            model_name=OLLAMA_EMBEDDING_MODEL,
        )

        # Initialize two collections: FAQ and Recommend
        self.faq_collection_name = "FAQ"
        self.recommend_collection_name = "Recommend"

        self._create_schema(self.faq_collection_name, is_faq=True)
        self._create_schema(self.recommend_collection_name, is_faq=False)

        # Initialize vector stores for FAQ and Recommend
        self.faq_vector_store = WeaviateVectorStore(
            weaviate_client=self.client,
            index_name=self.faq_collection_name,
            text_key="content",
            metadata_keys=["topic"],
        )

        self.recommend_vector_store = WeaviateVectorStore(
            weaviate_client=self.client,
            index_name=self.recommend_collection_name,
            text_key="content",
            metadata_keys=["topic", "product_id"],
        )

        self.faq_storage_context = StorageContext.from_defaults(
            vector_store=self.faq_vector_store
        )
        self.recommend_storage_context = StorageContext.from_defaults(
            vector_store=self.recommend_vector_store
        )

        self.faq_index = VectorStoreIndex.from_vector_store(
            self.faq_vector_store,
            embed_model=self.embed_model,
        ).as_retriever()

    def _create_schema(self, collection_name, is_faq: bool = False):
        try:
            self.client.collections.get(collection_name)
        except:
            schema = {
                "class": collection_name,
                "properties": [
                    {
                        "name": "content",
                        "dataType": ["string"],
                    },
                    {
                        "name": "topic",
                        "dataType": ["string"],
                    },
                ],
                "vectorizer": "none",
            }

            if not is_faq:
                schema["properties"].append(
                    {
                        "name": "product_id",
                        "dataType": ["uuid"],
                    }
                )

            self.client.collections.create_from_dict(schema)

            if is_faq and collection_name == self.faq_collection_name:
                self.load_faq()

    def load_faq(self):
        docs = []
        for faq in FAQ:
            docs.append(
                Document(
                    text=f"Question: {faq['question']} Answer: {faq['answer']}",
                    metadata={"topic": faq["topic"]},
                )
            )

        self.faq_index = VectorStoreIndex.from_documents(
            docs,
            storage_context=self.faq_storage_context,
            embed_model=self.embed_model,
        )

    @staticmethod
    def embedding_html(html_content: str):
        doc = BeautifulSoup(html_content, "html.parser")
        return doc.get_text()

    async def embedding_product(self, product: Product):
        try:
            all_cat_names_query = select(CategoryProduct).where(
                CategoryProduct.product_id == product.product_id
            )
            results = await self.db.execute(all_cat_names_query)
            results = results.scalars()

            cat_names = ""
            for cat in results:
                cat_names_query = select(Category).where(Category.cat_id == cat.cat_id)
                cat = await self.db.execute(cat_names_query)
                cat_names += cat.scalar_one_or_none().cat_name

            product_text = f"{product.product_name * 3} {cat_names * 2}"

            document = Document(
                text=product_text,
                metadata={"topic": "product", "product_id": str(product.product_id)},
            )

            _index = VectorStoreIndex.from_documents(
                [document],
                storage_context=self.recommend_storage_context,
                embed_model=self.embed_model,
            )

            return bool(_index)

        except Exception as e:
            logger.error(f"Error embedding product: {str(e)}")
            return False

    async def search_product(self, user_query: str):
        try:
            recommend_index = VectorStoreIndex.from_vector_store(
                self.recommend_vector_store,
                embed_model=self.embed_model,
            ).as_retriever()

            results = recommend_index.retrieve(user_query)
            if not results:
                return JSONResponse(
                    content={"Message": "No products found"},
                    status_code=status.HTTP_404_NOT_FOUND,
                )

            product_ids = []
            for product in results:
                product_id = product.node.metadata.get("product_id", None)
                if product_id:
                    product_ids.append(product_id)

            if not product_ids:
                return JSONResponse(
                    content={"Message": "No valid product IDs found"},
                    status_code=status.HTTP_404_NOT_FOUND,
                )

            product_get_query = select(Product).where(
                Product.product_id.in_(product_ids)
            )
            results = await self.db.execute(product_get_query)

           

            products = []
            for pro in results.scalars():
                products.append({"product_id": str(pro.product_id), "product_name" : pro.product_name, "product_price" : pro.price})
           

            return JSONResponse(content=products, status_code=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Search product error: {str(e)}")
            await self.db.rollback()
            return JSONResponse(
                content={"Message": f"Error: {str(e)}"},
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def embedding(self, docs: List[Document], is_faq: bool = False):
        storage_context = (
            self.faq_storage_context if is_faq else self.recommend_storage_context
        )

        index = VectorStoreIndex.from_documents(
            docs,
            storage_context=storage_context,
            embed_model=self.embed_model,
        )

        if is_faq:
            self.faq_index = index

    def query(self, query: str, top_k: int = 5, min_similarity: float = 0.5):
        index = self.faq_index

        results = index.retrieve(query)
        responses = []
        for node in results[:top_k] or []:
            if node.score >= min_similarity:
                responses.append({"text": node.text, "score": node.score})
        return responses

    def clear_collection(self, is_faq: bool = False):
        collection_name = (
            self.faq_collection_name if is_faq else self.recommend_collection_name
        )
        try:
            self.client.collections.delete(collection_name)
            self._create_schema(collection_name, is_faq=is_faq)
        except Exception as e:
            logger.error(f"Error clearing collection: {e}")

    def __del__(self):
        if hasattr(self, "client"):
            self.client.close()
