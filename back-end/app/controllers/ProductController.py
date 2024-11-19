from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.Products import Product
from serializers.ProductSerializers import *
from middlewares.token_config import *
from sqlalchemy import func, select
from sqlalchemy.dialects.postgresql import insert
from models.UserInterest import UserInterest, InterestScore
from models.Users import User
from models.Category import Category
from datetime import datetime
from models.CategoryProduct import CategoryProduct
from controllers.EmbeddingController import EmbeddingController
class ProductController:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def get_all_products(self):
        result = await self.db.execute(select(Product))
        return result.scalars().all()

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
            
    
    async def create_new_product(self, product: ProductCreate, current_user):
        try:
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
                create_at_datetime=product.create_at_datetime
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

            embedding_controller = EmbeddingController(self.db)
            await embedding_controller.embedding_product(db_product)

            return db_product
        except Exception as e:
            await self.db.rollback()
            raise e

    async def delete_existing_product(self, product_id, current_user):
        result = await self.db.execute(select(Product).filter(Product.product_id == product_id))
        db_product = result.scalar_one_or_none()
        if db_product:
            await self.db.delete(db_product)
            await self.db.commit()
        return db_product
