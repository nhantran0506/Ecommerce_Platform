from sqlalchemy.ext.asyncio import AsyncSession
from db_connector import get_db
from fastapi import Depends, status
from serializers.OrderSerializer import OderItems
from models.Users import User
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from models.Order import Order
from models.OrderItem import OrderItem
from models.Products import Product
from models.UserInterest import UserInterest, InterestScore
from datetime import datetime
from fastapi.responses import JSONResponse
from fastapi import HTTPException
from sqlalchemy import delete
from sqlalchemy import update
from models.Cart import Cart
from models.CartProduct import CartProduct
from helper_collections.VNPAY import get_vnpay_url
from serializers.ProductSerializers import VNPayPaymentCreate


class OrderController:

    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def order_product(
        self, order_items: list[OderItems], request, current_user: User
    ):
        try:
            # Get user's cart
            cart_query = select(Cart).where(Cart.user_id == current_user.user_id)
            result = await self.db.execute(cart_query)
            user_cart = result.scalar_one_or_none()

            if user_cart:
                # Get cart items to update
                cart_items_query = select(CartProduct).where(
                    CartProduct.cart_id == user_cart.cart_id
                )
                result = await self.db.execute(cart_items_query)
                cart_items = {item.product_id: item for item in result.scalars().all()}

                # Update cart quantities based on ordered items
                for order_item in order_items:
                    if order_item.product_id in cart_items:
                        cart_product = cart_items[order_item.product_id]
                        remaining_quantity = cart_product.quantity - order_item.quantity

                        if remaining_quantity > 0:
                            # Update cart quantity
                            update_query = (
                                update(CartProduct)
                                .where(
                                    CartProduct.cart_id == user_cart.cart_id,
                                    CartProduct.product_id == order_item.product_id,
                                )
                                .values(quantity=remaining_quantity)
                            )
                            await self.db.execute(update_query)
                        else:
                            # Remove item from cart if no quantity remains
                            delete_query = delete(CartProduct).where(
                                CartProduct.cart_id == user_cart.cart_id,
                                CartProduct.product_id == order_item.product_id,
                            )
                            await self.db.execute(delete_query)

            # Create new order
            user_order_create_query = (
                insert(Order)
                .values(user_id=current_user.user_id, created_at=datetime.now())
                .returning(Order.order_id)
            )
            result = await self.db.execute(user_order_create_query)
            order_id = result.scalar_one()

            # Process order items
            total_amount = 0
            for order_item in order_items:
                # Create order item
                query = insert(OrderItem).values(
                    order_id=order_id,
                    product_id=order_item.product_id,
                    quantity=order_item.quantity,
                )

                query = query.on_conflict_do_update(
                    index_elements=["order_id", "product_id"],
                    set_={"quantity": order_item.quantity},
                )

                # Update user interest
                insert_user_interest_query = (
                    insert(UserInterest)
                    .values(
                        product_id=order_item.product_id,
                        user_id=current_user.user_id,
                        score=InterestScore.BUY.value,
                    )
                    .on_conflict_do_update(
                        index_elements=["user_id", "product_id"],
                        set_={"score": InterestScore.BUY.value},
                    )
                )

                get_product_query = (
                    select(Product)
                    .where(Product.product_id == order_item.product_id)
                )
                product = await self.db.execute(get_product_query)
                product = product.scalar_one_or_none()
                if product:
                    total_amount += product.price * order_item.quantity

                await self.db.execute(query)
                await self.db.execute(insert_user_interest_query)

            try:
                payment = VNPayPaymentCreate(
                    amount=int(total_amount * 25377 * 100),
                    order_id=str(order_id),
                    order_desc=f"Order {str(order_id)}",
                )
                payment_url = await get_vnpay_url(payment, request)
            except Exception as e:
                await self.db.rollback()
                return JSONResponse(
                    content={"Error": str(e)},
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
            

            await self.db.commit()
            return JSONResponse(
                content={"payment_url": payment_url},
                status_code=status.HTTP_200_OK,
            )

        except Exception as e:
            await self.db.rollback()
            return JSONResponse(
                content={"Error": str(e)},
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    async def get_order_details(self, order_items: list[OderItems]):
        try:
            products = []
            for order_item in order_items:
                product_query = select(Product).where(
                    Product.product_id == order_item.product_id
                )
                result = await self.db.execute(product_query)
                product = result.scalar_one_or_none()

                if not product:
                    raise HTTPException(
                        status_code=404,
                        detail=f"Product with id {order_item.product_id} not found",
                    )

                products.append(
                    {
                        "product_name": product.product_name,
                        "product_id": order_item.product_id,
                        "quantity": order_item.quantity,
                        "price": product.price,
                        "total_price": order_item.quantity * product.price,
                    }
                )

            return {
                "order_details": {
                    "products": products,
                    "created_at": datetime.now(),
                }
            }
        except Exception as e:
            return JSONResponse(
                content={"Message": f"Error : {e}"},
                status_code=status.HTTP_401_UNAUTHORIZED,
            )

    async def order_products_all(self, request, current_user: User):
        try:
            # Get user's cart
            cart_query = select(Cart).where(Cart.user_id == current_user.user_id)
            result = await self.db.execute(cart_query)
            user_cart = result.scalar_one_or_none()

            if not user_cart:
                return JSONResponse(
                    content={"Message": "Cart is empty"},
                    status_code=status.HTTP_404_NOT_FOUND,
                )

            # Get cart items
            cart_items_query = select(CartProduct).where(
                CartProduct.cart_id == user_cart.cart_id
            )
            result = await self.db.execute(cart_items_query)
            cart_items = result.scalars().all()

            if not cart_items:
                return JSONResponse(
                    content={"Message": "Cart is empty"},
                    status_code=status.HTTP_404_NOT_FOUND,
                )

            # Create new order
            user_order_create_query = (
                insert(Order)
                .values(user_id=current_user.user_id, created_at=datetime.now())
                .returning(Order.order_id)
            )
            result = await self.db.execute(user_order_create_query)
            order_id = result.scalar_one()

            # Process each cart item
            total_amount = 0
            for cart_item in cart_items:
                # Create order item
                query = insert(OrderItem).values(
                    order_id=order_id,
                    product_id=cart_item.product_id,
                    quantity=cart_item.quantity,
                )

                query = query.on_conflict_do_update(
                    index_elements=["order_id", "product_id"],
                    set_={"quantity": cart_item.quantity},
                )

                # Update user interest
                insert_user_interest_query = (
                    insert(UserInterest)
                    .values(
                        product_id=cart_item.product_id,
                        user_id=current_user.user_id,
                        score=InterestScore.BUY.value,
                    )
                    .on_conflict_do_update(
                        index_elements=["user_id", "product_id"],
                        set_={"score": InterestScore.BUY.value},
                    )
                )

                get_product_query = (
                    select(Product)
                    .where(Product.product_id == cart_item.product_id)
                )
                product = await self.db.execute(get_product_query)
                product = product.scalar_one_or_none()
                total_amount += product.price * cart_item.quantity

                await self.db.execute(query)
                await self.db.execute(insert_user_interest_query)

            # Remove items from cart
            delete_cart_items_query = delete(CartProduct).where(
                CartProduct.cart_id == user_cart.cart_id
            )
            await self.db.execute(delete_cart_items_query)

            

            try:
                payment = VNPayPaymentCreate(
                    amount=int(total_amount * 25377 * 100),
                    order_id=str(order_id),
                    order_desc=f"Order {str(order_id)}",
                )
                payment_url = await get_vnpay_url(payment, request)
            except Exception as e:
                await self.db.rollback()
                return JSONResponse(
                    content={"Error": str(e)},
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
            
            await self.db.commit()
            return JSONResponse(
                content={"payment_url": payment_url},
                status_code=status.HTTP_200_OK,
            )

        except Exception as e:
            await self.db.rollback()
            return JSONResponse(
                content={"Error": str(e)},
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
    

    async def get_order_history(self, current_user : User):
        try:
            get_all_order_query = select(Order).where(Order.user_id == current_user.user_id)
            all_orders = await self.db.execute(get_all_order_query)
            all_orders = all_orders.scalars().all()

            response = {}

            for order in all_orders or []:
                get_orderItems = select(OrderItem).where(OrderItem.order_id == order.order_id)
                orderItems = await self.db.execute(get_orderItems)
                orderItems = orderItems.scalars().all()

                product_list_info = []

                for orderItem in orderItems or []:
                    get_product_query = select(Product).where(Product.product_id == orderItem.product_id)
                    product = await self.db.execute(get_product_query)
                    product = product.scalar_one_or_none()
                    if product:
                        product_list_info.append(
                            {
                                "product_id" : str(product.product_id),
                                "product_name" : product.product_name,
                                "product_description" : product.product_description,
                                "price" : product.price,
                                "quantity" : orderItem.quantity,
                                "total" : orderItem.quantity * product.price
                            }
                            
                        )

                response[str(order.order_id)] = {
                    "order_id" : str(order.order_id),
                    "product" : product_list_info,
                    "created_at" : str(order.created_at),
                }

            return JSONResponse(content=response, status_code=status.HTTP_200_OK)
        except Exception as e:
            await self.db.rollback()
            print(str(e))
            return JSONResponse(
                content={"error" :"Unable to get order history."},
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

