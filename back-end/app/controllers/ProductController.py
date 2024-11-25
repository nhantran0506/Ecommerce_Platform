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
    
    async def update_product(self, product_update : ProductBase, current_user : User):
        try:
            # check user
            get_shop = select(Shop).where(Shop.owner_id == current_user.user_id)
            shop_result = await self.db.execute(get_shop)
            shop_result = shop_result.scalar_one_or_none()

            if not shop_result:
                return JSONResponse(content="User don't have shop.", status_code=status.HTTP_404_NOT_FOUND)
            
            for cat in product_update.category:
                query_insert = update(Category).values(
                    cat_name=cat
                )
                await self.db.execute(query_insert)
                await self.db.commit()

            db_product = Product(
                product_name=product.product_name,
                product_description=product.product_description,
                price=product.price,
            )
            self.db.add(db_product)
            await self.db.commit()
            await self.db.refresh(db_product)

          
            for cat_name in product.category:
                cat_query = select(Category).where(Category.cat_name == cat_name)
                result = await self.db.execute(cat_query)
                category = result.scalar_one_or_none()
                
                if category:
                    
                    cat_product = CategoryProduct(
                        cat_id=category.cat_id,
                        product_id=db_product.product_id
                    )
                    self.db.add(cat_product)
                    await self.db.commit()
            
            product_shop_insert = insert(ShopProduct).values(
                product_id = db_product.product_id,
                shop_id = shop_result.shop_id,
            )
            await self.db.execute(product_shop_insert)
            await self.db.commit()
           

            embedding_controller = EmbeddingController(self.db)
            embedding_result = await embedding_controller.embedding_product(db_product)
            if not embedding_result:
                await self.db.rollback()
                logger.error(f"Embedding fail product {db_product.product_id}")
                return JSONResponse(content={"error" : "Can't save product"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
            

            return db_product
        except Exception as e:
            await self.db.rollback()
            logger.error(str(e))
            return JSONResponse(content={"error" : "Can't save product"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    async def create_new_product(self, product: ProductCreate, current_user : User):
        try:
            # check user
            get_shop = select(Shop).where(Shop.owner_id == current_user.user_id)
            shop_result = await self.db.execute(get_shop)
            shop_result = shop_result.scalar_one_or_none()

            if not shop_result:
                return JSONResponse(content="User don't have shop.", status_code=status.HTTP_404_NOT_FOUND)
            
            for cat in product.category:
                query_insert = insert(Category).values(
                    cat_name=cat
                ).on_conflict_do_nothing()
                await self.db.execute(query_insert)
                await self.db.commit()

            db_product = Product(
                product_name=product.product_name,
                product_description=product.product_description,
                price=product.price,
            )
            self.db.add(db_product)
            await self.db.commit()
            await self.db.refresh(db_product)

          
            for cat_name in product.category:
                cat_query = select(Category).where(Category.cat_name == cat_name)
                result = await self.db.execute(cat_query)
                category = result.scalar_one_or_none()
                
                if category:
                    
                    cat_product = CategoryProduct(
                        cat_id=category.cat_id,
                        product_id=db_product.product_id
                    )
                    self.db.add(cat_product)
                    await self.db.commit()
            
            product_shop_insert = insert(ShopProduct).values(
                product_id = db_product.product_id,
                shop_id = shop_result.shop_id,
            )
            await self.db.execute(product_shop_insert)
            await self.db.commit()
           

            embedding_controller = EmbeddingController(self.db)
            embedding_result = await embedding_controller.embedding_product(db_product)
            if not embedding_result:
                await self.db.rollback()
                logger.error(f"Embedding fail product {db_product.product_id}")
                return JSONResponse(content={"error" : "Can't save product"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
            

            return db_product
        except Exception as e:
            await self.db.rollback()
            logger.error(str(e))
            return JSONResponse(content={"error" : "Can't save product"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    async def delete_product(self, product_id: uuid.UUID, current_user: User):
        try:
            get_shop = select(Shop).where(Shop.owner_id == current_user.user_id)
            shop_result = await self.db.execute(get_shop)
            shop = shop_result.scalar_one_or_none()

            if not shop:
                return JSONResponse(
                    content={"message": "User doesn't have a shop"}, 
                    status_code=status.HTTP_404_NOT_FOUND
                )


            product_query = (
                select(Product)
                .join(ShopProduct, Product.product_id == ShopProduct.product_id)
                .where(
                    Product.product_id == product_id,
                    ShopProduct.shop_id == shop.shop_id
                )
            )
            result = await self.db.execute(product_query)
            product = result.scalar_one_or_none()

            if not product:
                return JSONResponse(
                    content={"message": "Product not found or doesn't belong to your shop"},
                    status_code=status.HTTP_404_NOT_FOUND
                )

            
            delete_cat_product = delete(CategoryProduct).where(
                CategoryProduct.product_id == product_id
            )
            await self.db.execute(delete_cat_product)

          
            delete_shop_product = delete(ShopProduct).where(
                ShopProduct.product_id == product_id
            )
            await self.db.execute(delete_shop_product)

        
            try:
                embedding_controller = EmbeddingController(self.db)
                embedding_result = await embedding_controller.delete_product(product)
                if not embedding_result:
                    await self.db.rollback()
                    return JSONResponse(
                        content={"message": f"Error deleting product: {str(e)}"},
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )
            except Exception as e:
                logger.warning(f"Error removing product from vector store: {str(e)}")
                
            
            await self.db.delete(product)
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
            
