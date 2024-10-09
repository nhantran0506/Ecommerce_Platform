from models.Users import User, UserRoles
from serializers.AdminSerializer import *
from middlewares.token_config import *
from fastapi.responses import JSONResponse, HTMLResponse
from sqlalchemy import func, select
from models.OrderItem import OrderItem
from fastapi import status
from datetime import datetime
from models.Shop import Shop
from sqlalchemy.ext.asyncio import AsyncSession
from models.Products import Product
import plotly.graph_objs as go
import calendar


class AdminController:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def get_revenue(self, admin_data: AdminGetData, current_user: User):
        # If role check is needed, uncomment the below section.
        # if current_user.role != UserRoles.ADMIN:
        #     return JSONResponse(
        #         content={"Message": "Invalid credentials."},
        #         status_code=status.HTTP_401_UNAUTHORIZED,
        #     )

        
        timestamp_str = admin_data.timestamp  
        try:
            start_date = datetime.strptime(timestamp_str, "%Y-%m")
        except ValueError:
            return JSONResponse(
                content={"Message": "Invalid date format, expected YYYY-MM."},
                status_code=400,
            )

        start_of_month = start_date.replace(day=1)
        _, last_day_of_month = calendar.monthrange(start_of_month.year, start_of_month.month)
        end_of_month = start_of_month.replace(day=last_day_of_month, hour=23, minute=59, second=59)

        query = select(OrderItem).where(
            OrderItem.order_at >= start_of_month, OrderItem.order_at <= end_of_month
        )
        result = await self.db.execute(query)
        orders_in_month = result.scalars().all()

        daily_revenue = {}
        for order in orders_in_month:
            product_query = select(Product).where(Product.product_id == order.product_id)
            result = await self.db.execute(product_query)
            product = result.scalar_one_or_none()

            if not product:
                continue

            total_price = order.quantity * product.price
            order_day = order.order_at.date()
            if order_day not in daily_revenue:
                daily_revenue[order_day] = 0
            daily_revenue[order_day] += total_price

        dates = sorted(daily_revenue.keys())
        revenues = [daily_revenue[date] for date in dates]

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=dates, y=revenues, mode="lines", name="Revenue"))

        chart_html = fig.to_html(full_html=False)

        return HTMLResponse(content=chart_html)

    async def statistics_product_category(
        self, category_name: str, timestamp: datetime
    ):
        pass  # -> quantity, total

    async def get_shop_number(self):
        query = select(func.count()).select_from(Shop)
        result = await self.db.execute(query)
        shop_count = result.scalar()
        return shop_count
