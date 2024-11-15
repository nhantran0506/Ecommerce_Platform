from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.Products import Product
from serializers.ProductSerializers import *
from middlewares.token_config import *
from sqlalchemy import func, select, insert
from models.UserInterest import UserInterest, InterestScore
class ProductController:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def get_all_products(self):
        result = await self.db.execute(select(Product))
        return result.scalars().all()

    async def get_single_product(self, product_id):
        
        # UserInterst insert
        interest_query = insert(UserInterest).values(
            user_id = current_user.user_id,
            product_id = product_id,
            score = InterestScore.VIEW
        )

        # below code need to change to new SQL base code
        result = await self.db.execute(select(Product).filter(Product.product_id == product_id))
        return result.scalar_one_or_none()

    async def create_new_product(self, product: ProductCreate, current_user):
        db_product = Product(**product.model_dump())
        self.db.add(db_product)
        await self.db.commit()
        await self.db.refresh(db_product)
        return db_product

    async def delete_existing_product(self, product_id, current_user):
        result = await self.db.execute(select(Product).filter(Product.product_id == product_id))
        db_product = result.scalar_one_or_none()
        if db_product:
            await self.db.delete(db_product)
            await self.db.commit()
        return db_product
