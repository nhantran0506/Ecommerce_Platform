from bs4 import BeautifulSoup
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Document
from llama_index.vector_stores.weaviate import WeaviateVectorStore
from llama_index.core import StorageContext
from llama_index.embeddings.ollama import OllamaEmbedding
import weaviate
from helper_collections.FAQQUES import FAQ
from typing import Optional, List
import asyncio
import aiohttp
from models.Products import *
from config import (
    OLLAMA_CHAT_MODEL,
    OLLAMA_BASE_URL,
    WEAVIATE_URL,
    OLLAMA_EMBEDDING_MODEL,
    VECTOR_DIMENSIONS,
    REDIS_TTL,
    CDN_GET_URL,
    CDN_SERVER_URL,
)
from models.CategoryProduct import CategoryProduct
from models.Category import Category
from models.Shop import Shop
from models.ShopProduct import ShopProduct
from sqlalchemy import select, update, insert
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from db_connector import get_db
from serializers.ProductSerializers import ProductResponse, SearchFilter
from llama_index.core.indices.vector_store.retrievers import VectorIndexRetriever
from fastapi import status
from fastapi.responses import JSONResponse
import weaviate.classes.query as wq
from llama_index.core.vector_stores import MetadataFilters, ExactMatchFilter
from llama_index.core.postprocessor import SimilarityPostprocessor
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
import logging
from redis_config import get_redis
import json


logger = logging.getLogger(__name__)


class EmbeddingController:
    faq_collection_name = "FAQ"
    recommend_collection_name = "Recommend"

    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db
        self.redis = get_redis()
        try:
            self.client = weaviate.connect_to_local(
                host=WEAVIATE_URL,
                port=8080,
                # skip_init_checks=True,
            )

            self.embed_model_recommend = HuggingFaceEmbedding(
                model_name="BAAI/bge-small-en",
                device="cuda",
            )

            self.embed_model = OllamaEmbedding(
                model_name=OLLAMA_EMBEDDING_MODEL,
                base_url=OLLAMA_BASE_URL,
                request_timeout=500.0,
                dimensions=VECTOR_DIMENSIONS,
                show_progress=True,
            )

            self._create_schema(self.faq_collection_name, is_faq=True)
            self._create_schema(self.recommend_collection_name, is_faq=False)

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

            postprocessor = SimilarityPostprocessor(similarity_cutoff=0.4)
            self.faq_index = VectorStoreIndex.from_vector_store(
                self.faq_vector_store,
                embed_model=self.embed_model,
            ).as_retriever(similarity_top_k=256, node_postprocessors=[postprocessor])

            self.recommend_index = VectorStoreIndex.from_vector_store(
                self.recommend_vector_store,
                embed_model=self.embed_model_recommend,
            ).as_retriever(similarity_top_k=256, node_postprocessors=[postprocessor])
        except Exception as e:
            logger.error(str(e))

    async def _get_image(self, image_url: str) -> dict:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{CDN_SERVER_URL}/{CDN_GET_URL}/{image_url}"
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        return {"success": True, "image_url": result["image_url"]}
                    else:
                        return {
                            "success": False,
                            "error": f"Failed to retrieve image, status: {response.status}",
                        }
        except Exception as e:
            return {"success": False, "error": str(e)}

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
            results = results.scalars().all()

            cat_names = ""
            for cat in results:
                cat = await self.db.execute(
                    select(Category).where(Category.cat_id == cat.cat_id)
                )
                cat_data = cat.scalar_one_or_none()
                if cat_data:
                    cat_names += cat_data.cat_name.value

            product_text = (
                f"{' '.join([product.product_name] * 2)} {' '.join(cat_names * 1)}"
            )

            document = Document(
                text=product_text,
                metadata={"topic": "product", "product_id": str(product.product_id)},
            )

            _index = VectorStoreIndex.from_documents(
                [document],
                storage_context=self.recommend_storage_context,
                embed_model=self.embed_model_recommend,
                show_progress=True,
            )

            if hasattr(_index, "close"):
                _index.close()

            return True

        except Exception as e:
            logger.error(f"Error embedding product: {str(e)}")
            return False

    async def delete_product(self, product: Product):
        try:
            filters = MetadataFilters(
                filters=[
                    ExactMatchFilter(key="product_id", value=str(product.product_id))
                ]
            )

            _index = VectorStoreIndex.from_vector_store(
                self.recommend_vector_store,
                embed_model=self.embed_model_recommend,
            ).as_retriever(
                similarity_top_k=1, vector_store_query_mode="default", filters=filters
            )

            vector_result = _index.retrieve(" ")
            if vector_result:
                document_id = vector_result[0].node.id_
                self.recommend_vector_store.delete(document_id)
                return True
            else:
                await self.recommend_vector_store.async_add(vector_result[0].node)
                logger.error("No document found with the specified product_id.")
                return False

        except Exception as e:
            logger.error(f"Error removing product from vector store: {str(e)}")
            return False

    async def search_product(self, user_query: str, filters: Optional[SearchFilter] = None):
        try:
            filter_key = ""
            if filters:
                if filters.categories:
                    filter_key += f"_cat={'_'.join(sorted(filters.categories))}"
                if filters.min_price is not None:
                    filter_key += f"_min={filters.min_price}"
                if filters.max_price is not None:
                    filter_key += f"_max={filters.max_price}"
            
            cache_key = f"product_search:{hash(user_query)}{filter_key}"
            cached_data = self.redis.get(cache_key)

            if cached_data:
                return JSONResponse(
                    content=json.loads(cached_data), 
                    status_code=status.HTTP_200_OK
                )

        
            vector_result = self.recommend_index.retrieve(user_query)

            if not vector_result:
                return JSONResponse(
                    content={"Message": "No products found"},
                    status_code=status.HTTP_404_NOT_FOUND,
                )

    
            product_ids = []
            for obj in vector_result:
                product_id = obj.node.metadata["product_id"]
                if product_id:
                    product_ids.append(product_id)

            if not product_ids:
                return JSONResponse(
                    content={"Message": "No valid product IDs found"},
                    status_code=status.HTTP_404_NOT_FOUND,
                )

            products = []
            for pro_id in product_ids:
                
                get_product_query = select(Product).where(Product.product_id == pro_id)
                product_result = await self.db.execute(get_product_query)
                product = product_result.scalar_one_or_none()

                if not product:
                    continue

               
                if filters:
                    if filters.min_price is not None and product.price < filters.min_price:
                        continue
                    if filters.max_price is not None and product.price > filters.max_price:
                        continue

             
                get_cat_name = select(CategoryProduct).where(
                    CategoryProduct.product_id == pro_id
                )
                cat_product_result = await self.db.execute(get_cat_name)
                cat_product_names = cat_product_result.scalars().all()

                cat_names = []
               
                
                for cat in cat_product_names:
                    get_cat_name = select(Category).where(
                        Category.cat_id == cat.cat_id
                    )
                    cat_name_result = await self.db.execute(get_cat_name)
                    cat_name = cat_name_result.scalar_one_or_none()
                    if cat_name:
                        cat_names.append(cat_name.cat_name.value)

            
                if filters and filters.categories:
                    if not any(cat in filters.categories for cat in cat_names):
                        continue

             
                get_image_query = select(ImageProduct).where(
                    ImageProduct.product_id == pro_id
                )
                image_results = await self.db.execute(get_image_query)
                product_images = image_results.scalars().all()

                image_urls = []
                if product_images:
                    image_url_tasks = [
                        self._get_image(img.image_url) for img in product_images
                    ]
                    image_url_results = await asyncio.gather(*image_url_tasks)
                    image_urls = [
                        result["image_url"]
                        for result in image_url_results
                        if result["success"]
                    ]

            
                get_shop_name = select(ShopProduct).where(
                    ShopProduct.product_id == pro_id
                )
                shop_product_result = await self.db.execute(get_shop_name)
                shop_product = shop_product_result.scalar_one_or_none()

                if shop_product:
                    get_shop_query = select(Shop).where(
                        Shop.shop_id == shop_product.shop_id
                    )
                    shop_result = await self.db.execute(get_shop_query)
                    shop = shop_result.scalar_one_or_none()

                    products.append({
                        "product_id": str(product.product_id),
                        "product_name": product.product_name,
                        "product_price": product.price,
                        "product_total_sales": product.total_sales,
                        "image_urls": image_urls,
                        "product_description": product.product_description,
                        "product_category": cat_names,
                        "product_avg_stars": product.avg_stars,
                        "product_total_ratings": product.total_ratings,
                        "shop_name": {
                            "shop_id": str(shop.shop_id),
                            "shop_name": shop.shop_name,
                        },
                    })

            self.redis.setex(cache_key, REDIS_TTL, json.dumps(products))

            return JSONResponse(content=products, status_code=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Search product error: {str(e)}")
            await self.db.rollback()
            return JSONResponse(
                content={"Message": f"Error: {str(e)}"},
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def query(self, query: str, top_k: int = 5, min_similarity: float = 0.5):

        results = self.faq_index.retrieve(query)
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

    async def __aenter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if hasattr(self, "embed_model"):
            del self.embed_model
        if hasattr(self, "embed_model_recommend"):
            del self.embed_model_recommend
        if hasattr(self, "client"):
            self.client.close()