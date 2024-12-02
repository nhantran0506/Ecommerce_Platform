from serializers.UserSearializers import *
from middlewares.token_config import *
from fastapi.responses import JSONResponse
from fastapi import status, Depends
from serializers.CartSerializer import *
from typing import List
from sqlalchemy import select, delete
from sqlalchemy.dialects.postgresql import insert
from models.Cart import Cart
from models.Products import Product
from models.CartProduct import CartProduct
from models.Shop import Shop
from models.UserInterest import UserInterest, InterestScore
from models.ShopProduct import ShopProduct
from sqlalchemy.ext.asyncio import AsyncSession
import logging
logger = logging.getLogger(__name__)


class CartController:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def update_cart(self, product_list: List[CartModify], current_user: User):
        try:
            user_cart_query = select(Cart).where(Cart.user_id == current_user.user_id)
            result = await self.db.execute(user_cart_query)
            user_cart = result.scalar_one_or_none()
            if user_cart is None:
                user_cart_create_query = insert(Cart).values(
                    user_id=current_user.user_id, created_at=datetime.now()
                )
                await self.db.execute(user_cart_create_query)
            
            get_user_shop_query = select(Shop).where(Shop.owner_id == current_user.user_id)
            shop = await self.db.execute(get_user_shop_query)
            shop = shop.scalar_one_or_none()

            result = await self.db.execute(user_cart_query)
            user_cart = result.scalar_one_or_none()
            for cart_items in product_list:
                if cart_items.quantity > 0:

                    # if shop:
                    #     check_user_shop_product_query = select(ShopProduct).where(ShopProduct.product_id == cart_items.product_id)
                    #     check_user_shop_product = await self.db.execute(check_user_shop_product_query)
                    #     check_user_shop_product = check_user_shop_product.scalar_one_or_none()
                    #     if check_user_shop_product:
                    #         return JSONResponse(
                    #             content={"error" : "Shopper can not buy their own product."},
                    #             status_code=status.HTTP_403_FORBIDDEN
                    #         )



                    query = insert(CartProduct).values(
                        cart_id=user_cart.cart_id,
                        product_id=cart_items.product_id,
                        quantity=cart_items.quantity,
                    ).on_conflict_do_update(
                        index_elements=["cart_id", "product_id"],
                        set_={"quantity": cart_items.quantity},
                    )

                    await self.db.execute(query)

                    insert_user_interest = insert(UserInterest).values(
                        user_id=current_user.user_id,
                        product_id=cart_items.product_id,
                        score=InterestScore.CART.value
                    ).on_conflict_do_update(
                        index_elements=["user_id", "product_id"],
                        set_={"score": InterestScore.CART.value}
                    )

                    await self.db.execute(insert_user_interest)
                else:
                    query = delete(CartProduct).where(
                        CartProduct.cart_id == user_cart.cart_id
                    )

            
            await self.db.commit()

            return await self.get_cart_details(current_user)

        except Exception as e:
            await self.db.rollback()
            logger.error(str(e))
            return JSONResponse(
                content={"Message": f"Error : {e}"},
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    async def get_cart_details(self, current_user: User):
        try:
            query = select(Cart).where(Cart.user_id == current_user.user_id)
            result = await self.db.execute(query)
            user_cart = result.scalar_one_or_none()

            if user_cart is None:
                user_cart_create_query = insert(Cart).values(
                    user_id=current_user.user_id, created_at=datetime.now()
                )
                await self.db.execute(user_cart_create_query)
                await self.db.commit()

            result = await self.db.execute(query)
            user_cart = result.scalar_one_or_none()

            cart_product_query = select(CartProduct).where(
                CartProduct.cart_id == user_cart.cart_id
            )
            result = await self.db.execute(cart_product_query)
            cart_items = result.scalars().all()

            cart_items_details = []
            total_price = 0
            for items in cart_items:
                product_query = select(Product).where(
                    Product.product_id == items.product_id
                )
                result = await self.db.execute(product_query)
                product = result.scalar_one_or_none()

                if not product:
                    raise HTTPException(
                        status_code=404,
                        detail=f"Product with id {items.product_id} not found",
                    )

                cart_items_details.append(
                    {
                        "product_name": product.product_name,
                        "product_id": product.product_id,
                        "quantity": items.quantity,
                        "price": product.price,
                        "total_price": items.quantity * product.price,
                    }
                )
                total_price += items.quantity * product.price

            return {
                "cart_details": {
                    "products": cart_items_details,
                    "created_at": datetime.now(),
                    "total_price": total_price
                }
            }
        except Exception as e:
            await self.db.rollback()
            logger.error(e)
            return JSONResponse(
                content={"Message": f"Error : {e}"},
                status_code=status.HTTP_401_UNAUTHORIZED,
            )
    

    async def cart_buy(self, cureent_user):
        pass
