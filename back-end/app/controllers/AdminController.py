from models.Users import User, UserRoles
from serializers.AdminSerializer import *
from middlewares.token_config import *
from fastapi.responses import JSONResponse, HTMLResponse
from sqlalchemy import func, select, insert
from models.OrderItem import OrderItem
from models.CategoryProduct import CategoryProduct
from models.Category import Category
from fastapi import status
from datetime import datetime
from models.Shop import Shop
from sqlalchemy.ext.asyncio import AsyncSession
from models.Products import Product
import plotly.graph_objs as go
import calendar
import pandas as pd
import logging


logger = logging.getLogger(__name__)


class AdminController:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def get_number_user(self, current_user: User):
        if current_user.role != UserRoles.ADMIN:
            return JSONResponse(
                content={"Message": "Invalid credentials."},
                status_code=status.HTTP_401_UNAUTHORIZED,
            )

        try:
            query = select(User).where(User.deleted_date != None)
            result = await self.db.execute(query)
            users = result.scalars().all()

            return JSONResponse(
                content={"results": str(len(users))},
                status_code=status.HTTP_200_OK,
            )
        except Exception as e:
            await self.db.rollback()
            logger.error(str(e))
            return JSONResponse(
                content={"Error": "Error with the server."},
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    async def get_number_shops(self, current_user: User):
        if current_user.role != UserRoles.ADMIN:
            return JSONResponse(
                content={"Message": "Invalid credentials."},
                status_code=status.HTTP_401_UNAUTHORIZED,
            )

        try:
            query = select(func.count(Shop.shop_id))
            result = await self.db.execute(query)
            count = result.scalar()

            return JSONResponse(
                content={"results": str(count)},
                status_code=status.HTTP_200_OK,
            )
        except Exception as e:
            await self.db.rollback()
            logger.error(str(e))
            return JSONResponse(
                content={"Error": "Error with the server."},
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    async def get_current_revenue(self, current_user: User):
        if current_user.role != UserRoles.ADMIN:
            return JSONResponse(
                content={"Message": "Invalid credentials."},
                status_code=status.HTTP_401_UNAUTHORIZED,
            )

        try:
            timestamp_str = datetime.now().strftime("%Y-%m")
            try:
                start_date = datetime.strptime(timestamp_str, "%Y-%m")
            except ValueError:
                return JSONResponse(
                    content={"Message": "Invalid date format, expected YYYY-MM."},
                    status_code=400,
                )

            start_of_month = start_date.replace(day=1)
            _, last_day_of_month = calendar.monthrange(
                start_of_month.year, start_of_month.month
            )
            end_of_month = start_of_month.replace(
                day=last_day_of_month, hour=23, minute=59, second=59
            )

            query = select(OrderItem).where(
                OrderItem.order_at >= start_of_month, OrderItem.order_at <= end_of_month
            )
            result = await self.db.execute(query)
            orders_in_month = result.scalars().all()

            total_price = 0.0
            for order in orders_in_month:
                product_query = select(Product).where(
                    Product.product_id == order.product_id
                )
                result = await self.db.execute(product_query)
                product = result.scalar_one_or_none()

                if not product:
                    continue

                total_price = order.quantity * product.price

            return JSONResponse(
                content={"results": str(total_price)},
                status_code=status.HTTP_200_OK,
            )
        except Exception as e:
            await self.db.rollback()
            logger.error(str(e))
            return JSONResponse(
                content={"Error": "Error with the server."},
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    async def create_admin(self, admin_data: AdminCreate, current_user: User):
        if current_user.role != UserRoles.ADMIN:
            return JSONResponse(
                content={"Message": "Invalid credentials."},
                status_code=status.HTTP_401_UNAUTHORIZED,
            )

        try:
            query = (
                insert(User)
                .values(
                    first_name=admin_data.first_name,
                    last_name=admin_data.last_name,
                    email=admin_data.username,
                    dob=admin_data.dob,
                    role=UserRoles.ADMIN,
                )
                .returning(User)
            )

            result = await self.db.execute(query)
            user = result.scalar_one_or_none()

            query_auth = insert(Authentication).values(
                user_id=user.user_id,
                user_name=user.phone_number,
                hash_pwd=await Authentication.hash_password(admin_data.password),
            )

            await self.db.execute(query_auth)
            await self.db.commit()

            return JSONResponse(
                content={"Message": "Create admin successfully!."},
                status_code=status.HTTP_201_CREATED,
            )
        except Exception as e:
            await self.db.rollback()
            logger.error(str(e))
            return JSONResponse(
                content={"Error": "Error with the server."},
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    async def statistics_income(self, admin_data: AdminGetData, current_user: User):
        if current_user.role != UserRoles.ADMIN:
            return JSONResponse(
                content={"Message": "Invalid credentials."},
                status_code=status.HTTP_401_UNAUTHORIZED,
            )

        timestamp_dt = admin_data.timestamp
        year = timestamp_dt.year
        month = timestamp_dt.month
        day = timestamp_dt.day
        today = datetime.today()
        start_of_month = datetime(year, month, 1)
        if year == today.year and month == today.month and day == today.day:
            end_of_month = datetime(year, month, day, 23, 59, 59)
        else:
            _, last_day_of_month = calendar.monthrange(year, month)
            end_of_month = datetime(year, month, last_day_of_month, 23, 59, 59)
        date_range = pd.date_range(
            start=start_of_month,
            end=end_of_month,
        )
        daily_revenue = {date.date(): 0 for date in date_range}

        try:
            query = select(OrderItem).where(
                OrderItem.order_at >= start_of_month, OrderItem.order_at <= end_of_month
            )
            result = await self.db.execute(query)
            orders_in_month = result.scalars().all()

            for order in orders_in_month:
                product_query = select(Product).where(
                    Product.product_id == order.product_id
                )
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

            fig.update_layout(xaxis_title="Date", yaxis_title="Income")

            chart_html = fig.to_html(
                full_html=False,
                config={
                    "displaylogo": False,
                },
            )

            return HTMLResponse(content=chart_html)
        except Exception as e:
            await self.db.rollback()
            logger.error(str(e))

            dates = sorted(daily_revenue.keys())
            revenues = [daily_revenue[date] for date in dates]

            blank_fig = go.Figure()
            blank_fig.add_trace(
                go.Scatter(x=dates, y=revenues, mode="lines", name="Revenue")
            )

            blank_fig.update_layout(xaxis_title="Date", yaxis_title="Income")

            blank_chart_html = blank_fig.to_html(
                full_html=False,
                config={
                    "displaylogo": False,
                },
            )

            return HTMLResponse(
                content=blank_chart_html,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    async def statistics_category(self, admin_data: AdminGetData, current_user: User):
        if current_user.role != UserRoles.ADMIN:
            return JSONResponse(
                content={"Message": "Invalid credentials."},
                status_code=status.HTTP_401_UNAUTHORIZED,
            )

        timestamp_dt = admin_data.timestamp
        year = timestamp_dt.year
        month = timestamp_dt.month
        day = timestamp_dt.day
        today = datetime.today()
        start_of_month = datetime(year, month, 1)
        if year == today.year and month == today.month and day == today.day:
            end_of_month = datetime(year, month, day, 23, 59, 59)
        else:
            _, last_day_of_month = calendar.monthrange(year, month)
            end_of_month = datetime(year, month, last_day_of_month, 23, 59, 59)
        date_range = pd.date_range(
            start=start_of_month,
            end=end_of_month,
        )

        try:
            query = select(OrderItem).where(
                OrderItem.order_at >= start_of_month, OrderItem.order_at <= end_of_month
            )
            result = await self.db.execute(query)
            orders_in_month = result.scalars().all()

            cat_query = select(Category)
            result = await self.db.execute(cat_query)
            all_categories = result.scalars().all()
            cats_name = [cat.cat_name for cat in all_categories]

            cats_income = {
                date.date(): {cat: 0 for cat in cats_name} for date in date_range
            }

            for order in orders_in_month:
                cat_product_query = select(CategoryProduct).where(
                    CategoryProduct.product_id == order.product_id
                )
                result = await self.db.execute(cat_product_query)
                cat_product = result.scalar_one_or_none()

                if not cat_product:
                    continue

                cat_query = select(Category).where(
                    Category.cat_id == cat_product.cat_id
                )
                result = await self.db.execute(cat_query)
                cat = result.scalar_one_or_none()

                if not cat:
                    continue

                product_query = select(Product).where(
                    Product.product_id == order.product_id
                )
                result = await self.db.execute(product_query)
                product = result.scalar_one_or_none()

                if not product:
                    continue

                total_price = order.quantity * product.price
                order_day = order.order_at.date()

                cats_income[order_day][cat.cat_name] += total_price

            dates = sorted(cats_income.keys())
            percentage_incomes_by_cat = {cat: [] for cat in cats_name}

            for date in dates:
                total_income = sum(cats_income[date].values())
                if total_income == 0:
                    for cat in cats_name:
                        percentage_incomes_by_cat[cat].append(0)
                else:
                    for cat in cats_name:
                        percentage = (cats_income[date][cat] / total_income) * 100
                        percentage_incomes_by_cat[cat].append(percentage)

            fig = go.Figure()

            for cat in cats_name:
                fig.add_trace(
                    go.Scatter(
                        x=dates,
                        y=percentage_incomes_by_cat[cat],
                        mode="lines",
                        stackgroup="one",
                        name=cat,
                    )
                )

            fig.update_layout(
                xaxis_title="Date",
                yaxis_title="Percentage of Total Income",
                yaxis=dict(range=[0, 100], tickformat=".0f"),
                showlegend=True,
            )

            chart_html = fig.to_html(
                full_html=False,
                config={"displaylogo": False},
            )

            return HTMLResponse(content=chart_html)

        except Exception as e:
            await self.db.rollback()
            logger.error(str(e))

            blank_fig = go.Figure()
            blank_fig.update_layout(
                xaxis_title="Date", yaxis_title="Percentage of Total Income"
            )
            blank_chart_html = blank_fig.to_html(
                full_html=False,
                config={"displaylogo": False},
            )

            return HTMLResponse(
                content=blank_chart_html,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    async def statistics_number_orders(
        self, admin_data: AdminCreate, current_user: User
    ):
        if current_user.role != UserRoles.ADMIN:
            return JSONResponse(
                content={"Message": "Invalid credentials."},
                status_code=status.HTTP_401_UNAUTHORIZED,
            )

        timestamp_dt = admin_data.timestamp
        year = timestamp_dt.year
        month = timestamp_dt.month
        day = timestamp_dt.day
        today = datetime.today()
        start_of_month = datetime(year, month, 1)
        if year == today.year and month == today.month and day == today.day:
            end_of_month = datetime(year, month, day, 23, 59, 59)
        else:
            _, last_day_of_month = calendar.monthrange(year, month)
            end_of_month = datetime(year, month, last_day_of_month, 23, 59, 59)
        date_range = pd.date_range(
            start=start_of_month,
            end=end_of_month,
        )

        try:
            query = select(OrderItem).where(
                OrderItem.order_at >= start_of_month, OrderItem.order_at <= end_of_month
            )
            result = await self.db.execute(query)
            orders_in_month = result.scalars().all()

            daily_orders = {date.date(): 0 for date in date_range}

            for order in orders_in_month:

                order_day = order.order_at.date()
                if order_day not in daily_orders:
                    daily_orders[order_day] = 0

                daily_orders[order_day] += 1

            dates = sorted(daily_orders.keys())
            num_orders = [daily_orders[date] for date in dates]

            fig = go.Figure()
            fig.add_trace(
                go.Scatter(x=dates, y=num_orders, mode="lines", name="Revenue")
            )

            fig.update_layout(xaxis_title="Date", yaxis_title="Number of Orders")

            chart_html = fig.to_html(
                full_html=False,
                config={
                    "displaylogo": False,
                },
            )

            return HTMLResponse(content=chart_html)

        except Exception as e:
            await self.db.rollback()
            logger.error(str(e))

            blank_fig = go.Figure()
            blank_fig.update_layout(xaxis_title="Date", yaxis_title="Number of Orders")
            blank_chart_html = blank_fig.to_html(
                full_html=False,
                config={"displaylogo": False},
            )

            return HTMLResponse(
                content=blank_chart_html,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
