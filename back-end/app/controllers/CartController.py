from serializers.UserSearializers import *
from middlewares.token_config import *
from fastapi.responses import JSONResponse
from fastapi import status, Depends
from serializers.CartSerializer import *
from typing import List
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from models.Cart import Cart
from models.CartProduct import CartProduct
from sqlalchemy.ext.asyncio import AsyncSession

class CartController():
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db
    
    async def update_cart(self, product_list: List[CartModify], current_user: User):
        try:
            user_cart_query = select(Cart).where(Cart.user_id == current_user.user_id)
            result = await self.db.execute(user_cart_query)
            user_cart = result.scalar_one_or_none()
            if user_cart is None:
                user_cart_create_query = insert(Cart).values(
                    user_id=current_user.user_id,
                    created_at=datetime.now()
                )
                await self.db.execute(user_cart_create_query)
                await self.db.commit()

            result = await self.db.execute(user_cart_query)
            user_cart = result.scalar_one_or_none()
            for cart_items in product_list:
                query = insert(CartProduct).values(
                    cart_id = user_cart.cart_id,
                    product_id = cart_items.product_id,
                    quantity = cart_items.quantity,
                )

                query = query.on_conflict_do_update(
                    index_elements=['cart_id', 'product_id'],  
                    set_={'quantity': cart_items.quantity}     
                )

                await self.db.execute(query)
                await self.db.commit()
            
            return JSONResponse(
                content={"Adding products successfully!."},
                status_code=status.HTTP_200_OK,
            )
        
        except Exception as e:
            await self.db.rollback()
            return JSONResponse(
                content={"Message": f"Error : {e}"},
                status_code=status.HTTP_401_UNAUTHORIZED,
            )