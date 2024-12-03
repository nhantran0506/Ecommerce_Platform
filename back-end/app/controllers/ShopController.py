from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from sqlalchemy.dialects.postgresql import insert
from fastapi.responses import JSONResponse
from models.Shop import Shop
from models.Ratings import ShopRating
from serializers.ShopSerializers import *
from middlewares.token_config import *
from sqlalchemy import func
import logging

logger = logging.getLogger(__name__)
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

    async def shop_rating(self, shop_rating: ShopRatingSerializer, current_user: User):
        try:
            # First check if shop exists
            get_shop_query = select(Shop).where(Shop.shop_id == shop_rating.shop_id)
            shop_result = await self.db.execute(get_shop_query)
            shop = shop_result.scalar_one_or_none()

            if not shop:
                return JSONResponse(
                    content={"error": "Shop not found"}, 
                    status_code=status.HTTP_404_NOT_FOUND
                )

            # Check if user has already rated this shop
            existing_rating_query = select(ShopRating).where(
                ShopRating.shop_id == shop_rating.shop_id,
                ShopRating.user_id == current_user.user_id
            )
            existing_rating_result = await self.db.execute(existing_rating_query)
            existing_rating = existing_rating_result.scalar_one_or_none()

            if existing_rating:
                # Update existing rating without changing timestamp
                update_rating_query = update(ShopRating).where(
                    ShopRating.shop_id == shop_rating.shop_id,
                    ShopRating.user_id == current_user.user_id
                ).values(
                    rating_stars=shop_rating.rating,
                    comment=shop_rating.comment
                )
                await self.db.execute(update_rating_query)

                # Recalculate average rating
                rating_query = (
                    select(func.sum(ShopRating.rating_stars), func.count(ShopRating.rating_stars))
                    .where(ShopRating.shop_id == shop_rating.shop_id)
                )
                rating_result = await self.db.execute(rating_query)

                total_stars, count_stars = rating_result.one_or_none()
                new_avg = float(total_stars / count_stars) if count_stars else 0.0
                
                # Update shop's average rating
                update_shop_query = update(Shop).where(
                    Shop.shop_id == shop_rating.shop_id
                ).values(
                    avg_stars=new_avg
                )
                await self.db.execute(update_shop_query)
            else:
                # Insert new rating
                new_rating = ShopRating(
                    shop_id=shop_rating.shop_id,
                    user_id=current_user.user_id,
                    rating_stars=shop_rating.rating,
                    comment=shop_rating.comment
                )
                self.db.add(new_rating)

                
                new_avg = (shop.avg_stars * shop.total_ratings + shop_rating.rating) / (shop.total_ratings + 1)
                update_shop_query = update(Shop).where(
                    Shop.shop_id == shop_rating.shop_id
                ).values(
                    avg_stars=new_avg,
                    total_ratings=shop.total_ratings + 1
                )
                await self.db.execute(update_shop_query)

            await self.db.commit()
            return JSONResponse(
                content={"message": "Shop rated successfully"},
                status_code=status.HTTP_200_OK
            )
        except Exception as e:
            logger.error(str(e))
            await self.db.rollback()
            return JSONResponse(
                content={"error": "Failed to rate shop"},
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
