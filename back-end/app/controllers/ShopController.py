from sqlalchemy.orm import Session
from models.Shop import Shop
from serializers.ShopSerializers import *
from middlewares.token_config import *

class ShopController:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def get_all_shop(self):
        return self.db.query(Shop).all()


    def get_single_shop(self, shop_id: int):
        exist_shop = self.db.query(Shop).filter(Shop.shop_id == shop_id).first()
        
        if not exist_shop: 
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Shop with ID {shop_id} does not exist."
            )

        return exist_shop


    def create_new_shop(self, shop: ShopCreate, current_user):
        exist_shop = self.db.query(Shop).filter(Shop.owner_id == current_user.user_id).first()
        if exist_shop:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You already have a shop. Each user can only create one shop."
            )
        
        # Create new shop if no existing shop is found
        db_shop = Shop(**shop.model_dump(), owner_id=current_user.user_id)
        self.db.add(db_shop)
        self.db.commit()
        self.db.refresh(db_shop)
        return db_shop


    def delete_existing_shop(self, shop_id: int, current_user):
        db_shop = self.db.query(Shop).filter(Shop.shop_id == shop_id).first()
        if db_shop:
            self.db.delete(db_shop)
            self.db.commit()
        return db_shop
