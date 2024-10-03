from sqlalchemy import select, update, insert
from sqlalchemy.orm import Session
from models.Users import User, UserRoles
from models.Authentication import Authentication
from serializers.UserSearializers import *
from middlewares.token_config import *
from fastapi.responses import JSONResponse
from sqlalchemy.dialects.postgresql import UUID
from fastapi import status, Header, HTTPException, Security, Depends
from serializers.CartSerializer import *
from typing import List
from sqlalchemy import select, update, insert
from models.Cart import Cart

class CartController():
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db
    
    async def update_cart(self, product_list : List[CartModify], current_user : User):
        user_cart_query = select(Cart).where(Cart.user_id == current_user.user_id)
        user_cart = self.db.execute(user_cart_query).scalar_one_or_none()
        if user_cart is None:
            user_cart_create_query = insert(Cart).values(
                user_id = current_user.user_id,
                created_at = datetime.now()
            )
            await self.db.execute(user_cart_create_query)


        for cart_items in product_list:
             