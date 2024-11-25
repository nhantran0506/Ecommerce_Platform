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
from controllers.EmbeddingController import EmbeddingController
import logging

logger = logging.getLogger(__name__)



class ProductController:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def get_all_products(self):
        try:
            get_product_query = select(Product)
            result = await self.db.execute(get_product_query)
            results = result.scalars().all()
            return JSONResponse(content=results, status_code=status.HTTP_200_OK)
        except Exception as e:
            await self.db.rollback()
            return JSONResponse(content={"error" : "Internal error"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    async def get_single_product(self, product_id, current_user : User):
        try:
            product_check_query = select(Product).where(Product.product_id == product_id)
            product_check_result = await self.db.execute(product_check_query)
            product = product_check_result.scalar_one_or_none()

            if not product:
                raise ValueError(f"Product with id {product_id} does not exist.")
            
            interest_query = insert(UserInterest).values(
                user_id=current_user.user_id,
                product_id=product_id,
                score=InterestScore.VIEW.value
            ).on_conflict_do_update(
                index_elements=['user_id', 'product_id'],  
                set_={'score': UserInterest.score + InterestScore.VIEW.value, 'updated_at' : datetime.now()}  
            )
            
            await self.db.execute(interest_query)
            await self.db.commit()
            product_query = select(Product).where(Product.product_id == product_id)
            result = await self.db.execute(product_query)
            return result.scalar_one_or_none()
        except Exception as e:
            await self.db.rollback()

    async def update_product(self, product_update: ProductUpdateSerializer, current_user: User):
        try:
            # Check user's shop
            get_shop = select(Shop).where(Shop.owner_id == current_user.user_id)
            shop_result = await self.db.execute(get_shop)
            shop = shop_result.scalar_one_or_none()

            if not shop:
                return JSONResponse(
                    content={"message": "User doesn't have a shop."}, 
                    status_code=status.HTTP_404_NOT_FOUND
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
                    status_code=status.HTTP_404_NOT_FOUND
                )

            # Update product basic info
            existing_product.product_name = product_update.product_name
            existing_product.product_description = product_update.product_description
            existing_product.price = product_update.price

            # Remove existing categories
            delete_query = delete(CategoryProduct).where(
                CategoryProduct.product_id == product_update.product_id
            )
            await self.db.execute(delete_query)

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
                        detail=f"Category {cat_name} not found"
                    )
                
                cat_product = CategoryProduct(
                    cat_id=category.cat_id,
                    product_id=existing_product.product_id
                )
                self.db.add(cat_product)

            await self.db.commit()
            return JSONResponse(
                content={"message": "Product updated successfully"},
                status_code=status.HTTP_200_OK
            )

        except ValueError as e:
            await self.db.rollback()
            return JSONResponse(
                content={"message": str(e)},
                status_code=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            await self.db.rollback()
            return JSONResponse(
                content={"message": "An error occurred while updating the product"},
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    async def create_product(self, product: ProductBase, current_user: User):
        try:
            get_shop = select(Shop).where(Shop.owner_id == current_user.user_id)
            shop_result = await self.db.execute(get_shop)
            shop = shop_result.scalar_one_or_none()

            if not shop:
                return JSONResponse(
                    content={"message": "User doesn't have a shop."}, 
                    status_code=status.HTTP_404_NOT_FOUND
                )
            
            
            db_product_query = insert(Product).values(
                product_name=product.product_name,
                product_description=product.product_description,
                price=product.price,
            ).returning(Product)
            db_product = await self.db.execute(db_product_query)
            db_product = db_product.scalar_one_or_none()

            shop_product_query = insert(ShopProduct).values(
                shop_id=shop.shop_id,
                product_id=db_product.product_id
            ).on_conflict_do_nothing()
            
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
                        detail=f"Category {cat_name} not found"
                    )
                
                cat_product = CategoryProduct(
                    cat_id=category.cat_id,
                    product_id=db_product.product_id
                )
                self.db.add(cat_product)
            
            try:
                embedding_controller = EmbeddingController(self.db)
                embedding_result = await embedding_controller.embedding_product(db_product)
                if not embedding_result:
                    await self.db.rollback()
                    return JSONResponse(
                        content={"message": f"Error create product from vector store"},
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )
            except Exception as e:
                logger.warning(f"Error create product from vector store: {str(e)}")
            
            await self.db.commit()
            
            return JSONResponse(
                content={"message": "Product created successfully"},
                status_code=status.HTTP_201_CREATED
            )

        except ValueError as e:
            await self.db.rollback()
            return JSONResponse(
                content={"message": str(e)},
                status_code=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            await self.db.rollback()
            return JSONResponse(
                content={"message": "An error occurred while creating the product"},
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    async def delete_product(self, product_id: uuid.UUID, current_user: User):
        try:
            print(current_user.user_id)
            get_shop = select(Shop).where(Shop.owner_id == current_user.user_id)
            shop_result = await self.db.execute(get_shop)
            shop = shop_result.scalar_one_or_none()
            if not shop:
                return JSONResponse(
                    content={"message": "User doesn't have a shop"},
                    status_code=status.HTTP_404_NOT_FOUND
                )

            # Delete from dependent tables first
            product_shop_query = delete(ShopProduct).where(ShopProduct.product_id == product_id)
            await self.db.execute(product_shop_query)

            product_cat_query = delete(CategoryProduct).where(CategoryProduct.product_id == product_id)
            await self.db.execute(product_cat_query)

            # Now delete the product itself
            product_delete_query = delete(Product).where(Product.product_id == product_id).returning(Product)
            product_result = await self.db.execute(product_delete_query)
            product = product_result.scalar_one_or_none()

            if not product:
                return JSONResponse(
                    content={"message": "Product not found"},
                    status_code=status.HTTP_404_NOT_FOUND
                )

            # Handle external system clean-up (e.g., vector store)
            try:
                embedding_controller = EmbeddingController(self.db)
                embedding_result = await embedding_controller.delete_product(product)
                if not embedding_result:
                    await self.db.rollback()
                    return JSONResponse(
                        content={"message": f"Error deleting product from vector store"},
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )
            except Exception as e:
                logger.warning(f"Error removing product from vector store: {str(e)}")

            await self.db.commit()
            return JSONResponse(
                content={"message": "Product deleted successfully"},
                status_code=status.HTTP_200_OK
            )

        except Exception as e:
            logger.error(f"Error deleting product: {str(e)}")
            await self.db.rollback()
            return JSONResponse(
                content={"message": f"Error deleting product: {str(e)}"},
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

            
