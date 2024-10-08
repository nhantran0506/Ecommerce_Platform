from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.Shop import Shop
from serializers.ShopSerializers import *
from middlewares.token_config import *

class ShopController:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def get_all_shop(self):
        result = await self.db.execute(select(Shop))
        return result.scalars().all()

    async def get_single_shop(self, shop_id):
        result = await self.db.execute(select(Shop).filter(Shop.shop_id == shop_id))
        exist_shop = result.scalar_one_or_none()
        
        if not exist_shop: 
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Shop with ID {shop_id} does not exist."
            )

        return exist_shop

    async def create_new_shop(self, shop: ShopCreate, current_user):
        result = await self.db.execute(select(Shop).filter(Shop.owner_id == current_user.user_id))
        exist_shop = result.scalar_one_or_none()
        if exist_shop:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You already have a shop. Each user can only create one shop."
            )
        
        db_shop = Shop(**shop.model_dump(), owner_id=current_user.user_id)
        self.db.add(db_shop)
        await self.db.commit()
        await self.db.refresh(db_shop)
        return db_shop

    async def delete_existing_shop(self, shop_id, current_user):
        result = await self.db.execute(select(Shop).filter(Shop.shop_id == shop_id))
        db_shop = result.scalar_one_or_none()
        if db_shop:
            await self.db.delete(db_shop)
            await self.db.commit()
        return db_shop
