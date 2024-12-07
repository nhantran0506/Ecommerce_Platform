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
import aiohttp
from serializers.ProductSerializers import ProductResponse
import weaviate.classes.query as wq
import numpy as np
from config import (
    WEAVIATE_URL,
    OLLAMA_EMBEDDING_MODEL,
    OLLAMA_BASE_URL,
    REDIS_TTL,
    CDN_GET_URL,
    CDN_SERVER_URL,
)
import logging
from redis_config import get_redis
import json
from datetime import datetime, timedelta
from models.OrderItem import OrderItem
import asyncio
from models.ImageProduct import ImageProduct
from models.ShopProduct import ShopProduct
from models.Shop import Shop
from llama_index.embeddings.huggingface import HuggingFaceEmbedding


logger = logging.getLogger(__name__)


class RecommendedController:
    collection_name = "Recommend"

    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db
        self.redis = get_redis()
        try:
            self.client = weaviate.connect_to_local(host=WEAVIATE_URL, port=8080)
            
            self.embed_model = HuggingFaceEmbedding(
                model_name="BAAI/bge-small-en"
            )

            # self.embed_model = OllamaEmbedding(
            #     model_name=OLLAMA_EMBEDDING_MODEL,
            #     base_url=OLLAMA_BASE_URL,
            #     request_timeout=500.0,
            #     show_progress=True,
            # )

            

            self._vector_store = WeaviateVectorStore(
                weaviate_client=self.client,
                index_name=self.collection_name,
                text_key="content",
                metadata_keys=["topic", "product_id"],
            )
            self._storage_context = StorageContext.from_defaults(
                vector_store=self._vector_store
            )
            
            try:
                self.client.collections.get(self.collection_name)
            except:
                schema = {
                    "class": self.collection_name,
                    "properties": [
                        {
                            "name": "content",
                            "dataType": ["string"],
                        },
                        {
                            "name": "topic",
                            "dataType": ["string"],
                        },
                        {
                            "name": "product_id",
                            "dataType": ["string"],  
                            "indexSearchable": True,  
                        },
                        {
                            "name": "product_name",
                            "dataType": ["string"],  
                            "indexSearchable": True, 
                        },
                        {
                            "name": "product_cat",
                            "dataType": ["string"],  
                            "indexSearchable": True, 
                        },
                    ],
                    "vectorizer": "none",
                }
                self.client.collections.create_from_dict(schema)
                
            self._index = VectorStoreIndex.from_vector_store(
                self._vector_store,
                embed_model=self.embed_model,
            ).as_retriever()
        except Exception as e:
            if hasattr(self, "client"):
                self.client.close()

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


    def __del__(self):
        if hasattr(self, "client") and self.client is not None:
            self.client.close()

    async def get_recommed(self, current_user: User):
        try:
            cache_key = f"user_recommendations:{current_user.user_id}"
            cached_data = self.redis.get(cache_key)

            if cached_data:
                return JSONResponse(
                    content=json.loads(cached_data), status_code=status.HTTP_200_OK
                )

            current_date = datetime.now()
            thirty_days_ago = current_date - timedelta(days=30)

            orders_query = select(OrderItem).where(
                OrderItem.order_at >= thirty_days_ago,
                OrderItem.order_at <= current_date,
            )
            orders = await self.db.execute(orders_query)
            orders = orders.scalars().all()

            product_metrics = {}
            for order in orders:
                if order.product_id not in product_metrics:
                    product_metrics[order.product_id] = {
                        "total_orders": 0,
                        "total_quantity": 0,
                        "total_revenue": 0,
                    }

                product_query = select(Product).where(
                    Product.product_id == order.product_id
                )
                product = await self.db.execute(product_query)
                product = product.scalar_one_or_none()

                if product:
                    product_metrics[order.product_id]["total_orders"] += 1
                    product_metrics[order.product_id][
                        "total_quantity"
                    ] += order.quantity
                    product_metrics[order.product_id]["total_revenue"] += (
                        order.quantity * product.price
                    )

            query_user_interest = (
                select(UserInterest)
                .where(UserInterest.user_id == current_user.user_id)
                .order_by(desc(UserInterest.updated_at), desc(UserInterest.score))
                .limit(20)
            )
            result = await self.db.execute(query_user_interest)
            user_interests = result.scalars().all()

            if not user_interests:
                return await self.get_default_recommed()

            product_embedding_dict = {"product_name": [], "score": []}
            for user_interest in user_interests:
                product_query = select(Product).where(
                    Product.product_id == user_interest.product_id
                )
                product = await self.db.execute(product_query)
                product = product.scalar_one_or_none()

                if not product:
                    continue

                all_cat_names_query = select(CategoryProduct).where(
                    CategoryProduct.product_id == user_interest.product_id
                )
                results_cat = await self.db.execute(all_cat_names_query)
                results_cat = results_cat.scalars()

                cat_names = ""
                for cat in results_cat:
                    cat_names_query = select(Category).where(
                        Category.cat_id == cat.cat_id
                    )
                    cat = await self.db.execute(cat_names_query)
                    cat = cat.scalar_one_or_none()
                    if cat:
                        cat_names += cat.cat_name.value

                product_text = (
                    f"{' '.join([product.product_name] * 2)} {' '.join(cat_names * 1)}"
                )
                product_embedding_dict["product_name"].append(product_text)
                product_embedding_dict["score"].append(user_interest.score)

            embedding_vectors = self.embed_model.get_text_embedding_batch(
                texts=product_embedding_dict["product_name"], show_progress=True
            )
            embedding_vectors = np.array(embedding_vectors)
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
                limit=256,
                return_metadata=wq.MetadataQuery(score=True),
            )

            products = []
            for obj in vector_result.objects or []:
                product_id = obj.properties.get("product_id", None)
                if not product_id:
                    continue

                get_image_query = select(ImageProduct).where(
                    ImageProduct.product_id == product_id
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

                get_product_query = select(Product).where(
                    Product.product_id == product_id
                )
                product_result = await self.db.execute(get_product_query)
                product = product_result.scalar_one_or_none()

                if product:

                    trending_score = 0
                    if product_id in product_metrics:
                        metrics = product_metrics[product_id]
                        trending_score = (
                            metrics["total_orders"] * 0.3
                            + metrics["total_quantity"] * 0.4
                            + (metrics["total_revenue"] / 1000000) * 0.3
                        )

                    get_shop_product = select(ShopProduct).where(
                        ShopProduct.product_id == product_id
                    )
                    shop_product_result = await self.db.execute(get_shop_product)
                    shop_product = shop_product_result.scalar_one_or_none()

                    if shop_product:
                        get_shop_query = select(Shop).where(
                            Shop.shop_id == shop_product.shop_id
                        )
                        shop_result = await self.db.execute(get_shop_query)
                        shop = shop_result.scalar_one_or_none()

                        get_cat_product = select(CategoryProduct).where(
                            CategoryProduct.product_id == product_id
                        )
                        cat_product_result = await self.db.execute(get_cat_product)
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

                        products.append(
                            {
                                "product_id": str(product.product_id),
                                "product_name": product.product_name,
                                "product_price": product.price,
                                "product_total_sales": product.total_sales,
                                "image_urls": image_urls,
                                "product_description": product.product_description,
                                "product_category": cat_names,
                                "product_avg_stars": product.avg_stars,
                                "product_total_ratings": product.total_ratings,
                                "trending_score": trending_score,
                                "inventory" : product.inventory,
                                "shop_name": {
                                    "shop_id": str(shop.shop_id) if shop else None,
                                    "shop_name": shop.shop_name if shop else None,
                                },
                            }
                        )

            products.sort(key=lambda x: x["trending_score"], reverse=True)

            self.redis.setex(cache_key, REDIS_TTL, json.dumps(products))
            return JSONResponse(content=products, status_code=status.HTTP_200_OK)

        except Exception as e:
            await self.db.rollback()
            logger.error(str(e))
            return JSONResponse(
                content={"Message": "Error getting recommendations"},
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
    async def get_default_recommed(self):
        try:
            cache_key = "default_recommendations"
            cached_data = self.redis.get(cache_key)

            if cached_data:
                return JSONResponse(
                    content=json.loads(cached_data), status_code=status.HTTP_200_OK
                )

            current_date = datetime.now()
            thirty_days_ago = current_date - timedelta(days=30)

            orders_query = select(OrderItem).where(
                OrderItem.order_at >= thirty_days_ago,
                OrderItem.order_at <= current_date,
            )
            orders = await self.db.execute(orders_query)
            orders = orders.scalars().all()

            product_metrics = {}

            
            if not orders:
                get_products_list_query = select(Product).limit(256)
                products_lists_result = await self.db.execute(get_products_list_query)
                products = products_lists_result.scalars().all()

                response = []
                for product in products:
                    get_image_query = select(ImageProduct).where(
                        ImageProduct.product_id == product.product_id
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

                    get_shop_product = select(ShopProduct).where(
                        ShopProduct.product_id == product.product_id
                    )
                    shop_product_result = await self.db.execute(get_shop_product)
                    shop_product = shop_product_result.scalar_one_or_none()

                    shop = None
                    if shop_product:
                        get_shop_query = select(Shop).where(
                            Shop.shop_id == shop_product.shop_id
                        )
                        shop_result = await self.db.execute(get_shop_query)
                        shop = shop_result.scalar_one_or_none()

                    get_cat_product = select(CategoryProduct).where(
                        CategoryProduct.product_id == product.product_id
                    )
                    cat_product_result = await self.db.execute(get_cat_product)
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

                    response.append(
                        {
                            "product_id": str(product.product_id),
                            "product_name": product.product_name,
                            "product_price": product.price,
                            "product_total_sales": product.total_sales,
                            "image_urls": image_urls,
                            "product_description": product.product_description,
                            "product_category": cat_names,
                            "product_avg_stars": product.avg_stars,
                            "product_total_ratings": product.total_ratings,
                            "trending_score": 0, 
                            "inventory" : product.inventory,
                            "shop_name": {
                                "shop_id": str(shop.shop_id) if shop else None,
                                "shop_name": shop.shop_name if shop else None,
                            },
                        }
                    )

                self.redis.setex(cache_key, REDIS_TTL, json.dumps(response))
                return JSONResponse(content=response, status_code=status.HTTP_200_OK)

           
            for order in orders:
                if order.product_id not in product_metrics:
                    product_metrics[order.product_id] = {
                        "total_orders": 0,
                        "total_quantity": 0,
                        "total_revenue": 0,
                    }

                product_query = select(Product).where(
                    Product.product_id == order.product_id
                )
                product = await self.db.execute(product_query)
                product = product.scalar_one_or_none()

                if product:
                    product_metrics[order.product_id]["total_orders"] += 1
                    product_metrics[order.product_id][
                        "total_quantity"
                    ] += order.quantity
                    product_metrics[order.product_id]["total_revenue"] += (
                        order.quantity * product.price
                    )

            products = []
            for product_id, metrics in product_metrics.items():
                trending_score = (
                    metrics["total_orders"] * 0.3
                    + metrics["total_quantity"] * 0.4
                    + (metrics["total_revenue"] / 1000000) * 0.3
                )

                get_image_query = select(ImageProduct).where(
                    ImageProduct.product_id == product_id
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

                product_query = select(Product).where(Product.product_id == product_id)
                product = await self.db.execute(product_query)
                product = product.scalar_one_or_none()

                if product:
                    get_shop_product = select(ShopProduct).where(
                        ShopProduct.product_id == product_id
                    )
                    shop_product_result = await self.db.execute(get_shop_product)
                    shop_product = shop_product_result.scalar_one_or_none()

                    shop = None
                    if shop_product:
                        get_shop_query = select(Shop).where(
                            Shop.shop_id == shop_product.shop_id
                        )
                        shop_result = await self.db.execute(get_shop_query)
                        shop = shop_result.scalar_one_or_none()

                    get_cat_product = select(CategoryProduct).where(
                        CategoryProduct.product_id == product_id
                    )
                    cat_product_result = await self.db.execute(get_cat_product)
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

                    products.append(
                        {
                            "product_id": str(product.product_id),
                            "product_name": product.product_name,
                            "product_price": product.price,
                            "product_total_sales": product.total_sales,
                            "image_urls": image_urls,
                            "product_description": product.product_description,
                            "product_category": cat_names,
                            "product_avg_stars": product.avg_stars,
                            "product_total_ratings": product.total_ratings,
                            "trending_score": trending_score,
                            "inventory" : product.inventory,
                            "shop_name": {
                                "shop_id": str(shop.shop_id) if shop else None,
                                "shop_name": shop.shop_name if shop else None,
                            },
                        }
                    )

            products.sort(key=lambda x: x["trending_score"], reverse=True)
            response = products[:256]

            self.redis.setex(cache_key, REDIS_TTL, json.dumps(response))
            return JSONResponse(content=response, status_code=status.HTTP_200_OK)

        except Exception as e:
            return JSONResponse(
                content={"error": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


        except Exception as e:
            await self.db.rollback()
            logger.error(str(e))
            return JSONResponse(
                content={"Message": "Error getting recommendations"},
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
