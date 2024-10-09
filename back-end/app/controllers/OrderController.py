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
from datetime import datetime
from fastapi.responses import JSONResponse
from fastapi import HTTPException



class OrderController:

    def __init__(self, db : AsyncSession = Depends(get_db)):
        self.db = db
    
    async def order_product(self, order_items : list[OderItems], current_user : User):
        try:
            user_order_create_query = insert(Order).values(
                user_id=current_user.user_id,
                created_at=datetime.now()
            )
            result = await self.db.execute(user_order_create_query)
            await self.db.commit()
            order = result.scalar_one_or_none()

            for order_item in order_items:
                query = insert(OrderItem).values(
                    cart_id = order.order_id,
                    product_id = order_item.product_id,
                    quantity = order_item.quantity,
                )

                query = query.on_conflict_do_update(
                    index_elements=['order_id', 'product_id'],  
                    set_={'quantity': order_item.quantity}     
                )

                await self.db.execute(query)
                await self.db.commit()
            
            return JSONResponse(
                content={"Order successfully!."},
                status_code=status.HTTP_200_OK,
            )
        
        except Exception as e:
            await self.db.rollback()
            return JSONResponse(
                content={"Message": f"Error : {e}"},
                status_code=status.HTTP_401_UNAUTHORIZED,
            )
    
    async def get_order_details(self, order_items : list[OderItems]):
        try:
            products =[]
            for order_item in order_items:
                product_query = select(Product).where(Product.product_id == order_item.product_id)
                result = await self.db.execute(product_query)
                product = result.scalar_one_or_none()

                if not product:
                    raise HTTPException(status_code=404, detail=f"Product with id {order_item.product_id} not found")

                products.append({
                    "product_name" : product.product_name,
                    "product_id" : order_item.product_id,
                    "quantity" : order_item.quantity,
                    "total_price" : order_item.quantity * product.price
                })
            
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
        