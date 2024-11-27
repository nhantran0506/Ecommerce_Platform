from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse
from models.Products import Product
from serializers.ProductSerializers import *
from middlewares.token_config import *
from sqlalchemy import func, delete, select, update
from sqlalchemy.dialects.postgresql import insert
from models.UserInterest import UserInterest, InterestScore
from models.Users import User
from models.Category import Category
from models.Shop import Shop
from datetime import datetime
from models.CategoryProduct import CategoryProduct
from models.ShopProduct import ShopProduct
from models.ImageProduct import ImageProduct
from controllers.EmbeddingController import EmbeddingController
import aiohttp
import asyncio
from config import CDN_BASE_URL, CDN_UPLOAD_URL, CDN_GET_URL, CDN_DELETE_URL
import logging

logger = logging.getLogger(__name__)


class ProductController:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def get_all_products(self):
        try:
            get_product_query = (
                select(Product).limit(256).order_by(Product.create_at_datetime.desc())
            )
            result = await self.db.execute(get_product_query)
            results = result.scalars().all()

            if not results:
                return JSONResponse(content=[], status_code=status.HTTP_200_OK)

            image_queries = [
                select(ImageProduct).where(ImageProduct.product_id == pro.product_id)
                for pro in results
            ]

            image_results_list = await asyncio.gather(
                *[self.db.execute(query) for query in image_queries]
            )

            async def get_product_with_image(pro, image_results):
                product_images = image_results.scalars().all()
                
                cat_names = []
                query_get_cat = await self.db.execute(select(CategoryProduct).where(CategoryProduct.product_id == pro.product_id))
                for cat in query_get_cat.scalars().all():
                    cat_name = await self.db.execute(select(Category).where(Category.cat_id == cat.cat_id))
                    cat_name = cat_name.scalar_one_or_none()
                    if not cat_name:
                        continue
                    cat_names.append(cat_name.cat_name.value)
                
                image_urls = []
                if product_images:

                    image_url_inputs = [img.image_url for img in product_images]

                    image_url_tasks = [
                        self._get_image(image_url) for image_url in image_url_inputs
                    ]
                    image_url_results = await asyncio.gather(*image_url_tasks)

                    image_urls = [
                        result["image_url"]
                        for result in image_url_results
                        if result["success"]
                    ]

                return {
                    "product_id": str(pro.product_id),
                    "product_name": pro.product_name,
                    "product_price": pro.price,
                    "product_category" : cat_names,
                    "product_description" : pro.product_description,
                    "image_urls": image_urls,
                }

            response = await asyncio.gather(
                *[
                    get_product_with_image(pro, image_results)
                    for pro, image_results in zip(results, image_results_list)
                ]
            )

            return JSONResponse(content=response, status_code=status.HTTP_200_OK)

        except Exception as e:
            logger.error(str(e))
            await self.db.rollback()
            return JSONResponse(
                content={"error": "Internal server"},
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    async def get_single_product(self, product_id, current_user: User):
        try:
            # Check if product exists
            product_check_query = select(Product).where(
                Product.product_id == product_id
            )
            product_check_result = await self.db.execute(product_check_query)
            product = product_check_result.scalar_one_or_none()

            if not product:
                raise ValueError(f"Product with id {product_id} does not exist.")

            cat = await self.db.execute(select(CategoryProduct).where(CategoryProduct.product_id == product.product_id))
            cat = cat.scalar_one_or_none()
            
            cat_name = await self.db.execute(select(Category).where(Category.cat_id == cat.cat_id))
            cat_names = cat_name.scalars().all()
            cat_names = [cat.cat_name.value for cat in cat_names]

            # Record user interest
            interest_query = (
                insert(UserInterest)
                .values(
                    user_id=current_user.user_id,
                    product_id=product_id,
                    score=InterestScore.VIEW.value,
                )
                .on_conflict_do_update(
                    index_elements=["user_id", "product_id"],
                    set_={
                        "score": UserInterest.score + InterestScore.VIEW.value,
                        "updated_at": datetime.now(),
                    },
                )
            )
            await self.db.execute(interest_query)
            await self.db.commit()

            # Get product images
            image_query = select(ImageProduct).where(ImageProduct.product_id == product_id)
            image_results = await self.db.execute(image_query)
            product_images = image_results.scalars().all()

            # Get image URLs from CDN
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

            # Prepare response
            response = {
                "product_id": str(product.product_id),
                "product_name": product.product_name,
                "product_description": product.product_description,
                "product_category" : cat_names,
                "price": product.price,
                "image_urls": image_urls
            }

            return JSONResponse(content=response, status_code=status.HTTP_200_OK)

        except ValueError as e:
            await self.db.rollback()
            return JSONResponse(
                content={"message": str(e)},
                status_code=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(str(e))
            await self.db.rollback()
            return JSONResponse(
                content={"message": "Internal server error"},
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    async def _upload_image(self, image: UploadFile) -> dict:
        try:

            async with aiohttp.ClientSession() as session:
                form = aiohttp.FormData()
                form.add_field(
                    "image",
                    await image.read(),
                    filename=image.filename,
                    content_type=image.content_type,
                )
                async with session.post(
                    url=f"{CDN_BASE_URL}/{CDN_UPLOAD_URL}", data=form
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        logger.info(f"{CDN_BASE_URL}/{CDN_UPLOAD_URL}")
                        return {
                            "success": True,
                            "product_image": result["product_image"],
                        }
                    else:
                        return {
                            "success": False,
                            "error": f"Failed to upload {image.filename}, status: {response.status}",
                        }
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def _get_image(self, image_url: str) -> dict:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{CDN_BASE_URL}/{CDN_GET_URL}/{image_url}"
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

    async def _delete_image(self, image_url: str) -> dict:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.delete(
                    f"{CDN_BASE_URL}/{CDN_DELETE_URL}/{image_url}"
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        return {"success": True, "message": result["message"]}
                    else:
                        return {
                            "success": False,
                            "error": f"Failed to delete image, status: {response.status}",
                        }
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def update_product(
        self,
        product_update: ProductUpdateSerializer,
        image_list: list[UploadFile],
        current_user: User,
    ):
        try:
            # Check user's shop
            get_shop = select(Shop).where(Shop.owner_id == current_user.user_id)
            shop_result = await self.db.execute(get_shop)
            shop = shop_result.scalar_one_or_none()

            if not shop:
                return JSONResponse(
                    content={"message": "User doesn't have a shop."},
                    status_code=status.HTTP_404_NOT_FOUND,
                )

            # Get existing product
            product_query = select(Product).where(
                Product.product_id == product_update.product_id
            )
            result = await self.db.execute(product_query)
            existing_product = result.scalar_one_or_none()

            if not existing_product:
                return JSONResponse(
                    content={"message": "Product not found"},
                    status_code=status.HTTP_404_NOT_FOUND,
                )

            # Update product basic info
            existing_product.product_name = product_update.product_name
            existing_product.product_description = product_update.product_description
            existing_product.price = product_update.price

            # Remove existing categories
            delete_cat_query = delete(CategoryProduct).where(
                CategoryProduct.product_id == product_update.product_id
            )
            await self.db.execute(delete_cat_query)

            # Add new categories
            for cat_name in product_update.category:
                cat_query = select(Category).where(
                    Category.cat_name == CatTypes(cat_name)
                )
                result = await self.db.execute(cat_query)
                category = result.scalar_one_or_none()

                if not category:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Category {cat_name} not found",
                    )

                cat_product = CategoryProduct(
                    cat_id=category.cat_id, product_id=existing_product.product_id
                )
                self.db.add(cat_product)

            # Handle existing images
            existing_images_query = select(ImageProduct).where(
                ImageProduct.product_id == existing_product.product_id
            )
            existing_images_result = await self.db.execute(existing_images_query)
            existing_images = existing_images_result.scalars().all()

            # Prepare image deletion tasks
            image_deletion_tasks = []
            if existing_images:
                image_deletion_tasks = [
                    self._delete_image(img.image_url) for img in existing_images
                ]

            # Delete existing image entries from database
            delete_images_query = delete(ImageProduct).where(
                ImageProduct.product_id == existing_product.product_id
            )
            await self.db.execute(delete_images_query)

            # Upload new images
            new_image_tasks = []
            if image_list:
                new_image_tasks = [self._upload_image(img) for img in image_list]

            # Concurrently delete old images and upload new images
            deletion_results = []
            if image_deletion_tasks:
                deletion_results = await asyncio.gather(*image_deletion_tasks)

            upload_results = []
            if new_image_tasks:
                upload_results = await asyncio.gather(*new_image_tasks)

            # Log any failed deletions or uploads
            failed_deletions = [
                result for result in deletion_results if not result["success"]
            ]
            failed_uploads = [
                result for result in upload_results if not result["success"]
            ]

            if failed_deletions:
                logger.warning(f"Failed to delete some images: {failed_deletions}")

            if failed_uploads:
                logger.warning(f"Failed to upload some images: {failed_uploads}")

            # Add new image entries to database
            for upload_result in upload_results:
                if upload_result["success"]:
                    new_image = ImageProduct(
                        product_id=existing_product.product_id,
                        image_url=upload_result["product_image"],
                    )
                    self.db.add(new_image)

            # Commit changes
            await self.db.commit()

            return JSONResponse(
                content={
                    "message": "Product updated successfully",
                    "failed_deletions": len(failed_deletions),
                    "failed_uploads": len(failed_uploads),
                },
                status_code=status.HTTP_200_OK,
            )

        except ValueError as e:
            await self.db.rollback()
            return JSONResponse(
                content={"message": str(e)}, status_code=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Error updating product: {str(e)}")
            return JSONResponse(
                content={"message": "An error occurred while updating the product"},
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    async def create_product(
        self, product: ProductBase, image_list: list[UploadFile], current_user: User
    ):
        try:
            get_shop = select(Shop).where(Shop.owner_id == current_user.user_id)
            shop_result = await self.db.execute(get_shop)
            shop = shop_result.scalar_one_or_none()

            if not shop:
                return JSONResponse(
                    content={"message": "User doesn't have a shop."},
                    status_code=status.HTTP_404_NOT_FOUND,
                )

            upload_tasks = [self._upload_image(image) for image in image_list]
            upload_results_future = asyncio.ensure_future(asyncio.gather(*upload_tasks))

            db_product_query = (
                insert(Product)
                .values(
                    product_name=product.product_name,
                    product_description=product.product_description,
                    price=product.price,
                )
                .returning(Product)
            )
            db_product = await self.db.execute(db_product_query)
            db_product = db_product.scalar_one_or_none()

            shop_product_query = (
                insert(ShopProduct)
                .values(shop_id=shop.shop_id, product_id=db_product.product_id)
                .on_conflict_do_nothing()
            )

            await self.db.execute(shop_product_query)

            for cat_name in product.category:
                cat_query = select(Category).where(
                    Category.cat_name == CatTypes(cat_name)
                )
                result = await self.db.execute(cat_query)
                category = result.scalar_one_or_none()

                if not category:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Category {cat_name} not found",
                    )

                cat_product = CategoryProduct(
                    cat_id=category.cat_id, product_id=db_product.product_id
                )
                self.db.add(cat_product)

            try:
                embedding_controller = EmbeddingController(self.db)
                embedding_result = await embedding_controller.embedding_product(
                    db_product
                )
                if not embedding_result:
                    await self.db.rollback()
                    return JSONResponse(
                        content={"message": f"Error create product from vector store"},
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    )
            except Exception as e:
                logger.warning(f"Error create product from vector store: {str(e)}")

            upload_results = await upload_results_future

            # Handle successful uploads
            successful_uploads = [
                res for res in upload_results if res.get("success", False)
            ]
            for upload in successful_uploads:
                query_image_product = (
                    insert(ImageProduct)
                    .values(
                        image_url=upload["product_image"],
                        product_id=db_product.product_id,
                    )
                    .on_conflict_do_nothing()
                )

                await self.db.execute(query_image_product)

            failed_uploads = [
                res for res in upload_results if not res.get("success", False)
            ]

            if failed_uploads:
                await self.db.rollback()
                placeholder_message = "Some images failed to upload: " + ", ".join(
                    [fail["error"] for fail in failed_uploads]
                )
                logger.error(placeholder_message)
                return JSONResponse(
                    content={"message": f"Error create product because image"},
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            await self.db.commit()

            return JSONResponse(
                content={"message": "Product created successfully"},
                status_code=status.HTTP_201_CREATED,
            )

        except ValueError as e:
            await self.db.rollback()
            return JSONResponse(
                content={"message": str(e)}, status_code=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            await self.db.rollback()
            return JSONResponse(
                content={"message": "An error occurred while creating the product"},
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    async def delete_product(self, product_id: uuid.UUID, current_user: User):
        try:
            # Get the shop associated with the current user
            get_shop = select(Shop).where(Shop.owner_id == current_user.user_id)
            shop_result = await self.db.execute(get_shop)
            shop = shop_result.scalar_one_or_none()

            if not shop:
                return JSONResponse(
                    content={"message": "User doesn't have a shop"},
                    status_code=status.HTTP_404_NOT_FOUND,
                )

            # First, get all image URLs associated with the product
            get_image_urls = select(ImageProduct).where(
                ImageProduct.product_id == product_id
            )
            image_result = await self.db.execute(get_image_urls)
            product_images = image_result.scalars().all()

            # Prepare to delete images concurrently
            image_deletion_tasks = []
            if product_images:
                image_deletion_tasks = [
                    self._delete_image(img.image_url) for img in product_images
                ]

            # Delete from dependent tables first
            product_shop_query = delete(ShopProduct).where(
                ShopProduct.product_id == product_id
            )
            await self.db.execute(product_shop_query)

            product_cat_query = delete(CategoryProduct).where(
                CategoryProduct.product_id == product_id
            )
            await self.db.execute(product_cat_query)

            # Delete image entries from database
            image_delete_query = delete(ImageProduct).where(
                ImageProduct.product_id == product_id
            )
            await self.db.execute(image_delete_query)

            # Now delete the product itself
            product_delete_query = (
                delete(Product)
                .where(Product.product_id == product_id)
                .returning(Product)
            )
            product_result = await self.db.execute(product_delete_query)
            product = product_result.scalar_one_or_none()

            if not product:
                return JSONResponse(
                    content={"message": "Product not found"},
                    status_code=status.HTTP_404_NOT_FOUND,
                )

            if image_deletion_tasks:
                image_deletion_results = await asyncio.gather(*image_deletion_tasks)
                failed_deletions = [
                    result for result in image_deletion_results if not result["success"]
                ]
                if failed_deletions:
                    await self.db.rollback()
                    logger.warning(f"Failed to delete some images: {failed_deletions}")
                    return JSONResponse(
                        content={
                            "error": "Product delete fail due to image deletion failed"
                        },
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    )

            try:
                embedding_controller = EmbeddingController(self.db)
                embedding_result = await embedding_controller.delete_product(product)
                if not embedding_result:
                    await self.db.rollback()
                    return JSONResponse(
                        content={
                            "message": f"Error deleting product from vector store"
                        },
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    )
            except Exception as e:
                logger.warning(f"Error removing product from vector store: {str(e)}")

            await self.db.commit()
            return JSONResponse(
                content={"message": "Product deleted successfully"},
                status_code=status.HTTP_200_OK,
            )

        except Exception as e:
            logger.error(f"Error deleting product: {str(e)}")
            await self.db.rollback()
            return JSONResponse(
                content={"message": f"Error deleting product: {str(e)}"},
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
