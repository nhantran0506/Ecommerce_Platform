from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from sqlalchemy.dialects.postgresql import insert
from fastapi.responses import JSONResponse, HTMLResponse
from models.Ratings import ShopRating
from serializers.ShopSerializers import *
from middlewares.token_config import *
from sqlalchemy import func
import plotly.graph_objs as go
from models.Shop import Shop
from models.ShopProduct import ShopProduct
from models.OrderItem import OrderItem
from models.Products import Product
from models.Category import Category
from models.CategoryProduct import CategoryProduct
from models.Users import User, UserRoles
from serializers.ShopSerializers import *
from config import REDIS_TTL
from redis_config import get_redis
from datetime import datetime
import calendar
import pandas as pd
import logging

logger = logging.getLogger(__name__)


class ShopController:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db
        self.redis = get_redis()

    async def get_all_shop(self):
        result = await self.db.execute(select(Shop))
        return result.scalars().all()

    async def get_single_shop(self, shop_id):
        result = await self.db.execute(select(Shop).filter(Shop.shop_id == shop_id))
        exist_shop = result.scalar_one_or_none()

        if not exist_shop:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Shop with ID {shop_id} does not exist.",
            )

        return exist_shop

    async def create_new_shop(self, shop: ShopCreate, current_user : User):
        try:
            result = await self.db.execute(
                select(Shop).filter(Shop.owner_id == current_user.user_id)
            )
            exist_shop = result.scalar_one_or_none()
            if exist_shop:
                return JSONResponse(
                    status_code=status.HTTP_403_FORBIDDEN,
                    content={"error" : "You already have a shop. Each user can only create one shop."},
                )
            
            update_user_query = update(User).where(User.user_id == current_user.user_id).values(
                role = UserRoles.SHOP_OWNER,
            )
            await self.db.execute(update_user_query)
            
            create_new_shop_query = insert(Shop).values(
                shop_name = shop.shop_name,
                shop_address = shop.shop_address,
                shop_bio = shop.shop_bio,
                shop_phone_number = current_user.phone_number,
                owner_id=current_user.user_id
            ).returning(Shop)

            
            db_shop = await self.db.execute(create_new_shop_query)
            await self.db.commit()
            return db_shop
        except Exception as e:
            await self.db.rollback()
            logger.error(str(e))

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
                    status_code=status.HTTP_404_NOT_FOUND,
                )

            # Check if user has already rated this shop
            existing_rating_query = select(ShopRating).where(
                ShopRating.shop_id == shop_rating.shop_id,
                ShopRating.user_id == current_user.user_id,
            )
            existing_rating_result = await self.db.execute(existing_rating_query)
            existing_rating = existing_rating_result.scalar_one_or_none()

            if existing_rating:
                # Update existing rating without changing timestamp
                update_rating_query = (
                    update(ShopRating)
                    .where(
                        ShopRating.shop_id == shop_rating.shop_id,
                        ShopRating.user_id == current_user.user_id,
                    )
                    .values(
                        rating_stars=shop_rating.rating, comment=shop_rating.comment
                    )
                )
                await self.db.execute(update_rating_query)

                # Recalculate average rating
                rating_query = select(
                    func.sum(ShopRating.rating_stars),
                    func.count(ShopRating.rating_stars),
                ).where(ShopRating.shop_id == shop_rating.shop_id)
                rating_result = await self.db.execute(rating_query)

                total_stars, count_stars = rating_result.one_or_none()
                new_avg = float(total_stars / count_stars) if count_stars else 0.0

                # Update shop's average rating
                update_shop_query = (
                    update(Shop)
                    .where(Shop.shop_id == shop_rating.shop_id)
                    .values(avg_stars=new_avg)
                )
                await self.db.execute(update_shop_query)
            else:
                # Insert new rating
                new_rating = ShopRating(
                    shop_id=shop_rating.shop_id,
                    user_id=current_user.user_id,
                    rating_stars=shop_rating.rating,
                    comment=shop_rating.comment,
                )
                self.db.add(new_rating)

                new_avg = (shop.avg_stars * shop.total_ratings + shop_rating.rating) / (
                    shop.total_ratings + 1
                )
                update_shop_query = (
                    update(Shop)
                    .where(Shop.shop_id == shop_rating.shop_id)
                    .values(avg_stars=new_avg, total_ratings=shop.total_ratings + 1)
                )
                await self.db.execute(update_shop_query)

            await self.db.commit()
            return JSONResponse(
                content={"message": "Shop rated successfully"},
                status_code=status.HTTP_200_OK,
            )
        except Exception as e:
            logger.error(str(e))
            await self.db.rollback()
            return JSONResponse(
                content={"error": "Failed to rate shop"},
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    async def statistics_revenue(self, shop_data: ShopGetData, current_user: User):
        try:
            # Get shop owned by user
            shop_query = select(Shop).where(Shop.owner_id == current_user.user_id)
            result = await self.db.execute(shop_query)
            shop = result.scalar_one_or_none()

            if not shop:
                return JSONResponse(
                    content={"Message": "Shop not found"},
                    status_code=status.HTTP_404_NOT_FOUND,
                )

            # Cache key for this shop's revenue stats
            timestamp_dt = shop_data.timestamp
            cache_key = (
                f"shop:{shop.shop_id}:revenue_stats:{timestamp_dt.strftime('%Y-%m')}"
            )

            # Try to get cached statistics
            # cached_html = self.redis.get(cache_key)
            # if cached_html:
            #     return HTMLResponse(content=cached_html)

            # Calculate date range
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

            date_range = pd.date_range(start=start_of_month, end=end_of_month)
            daily_revenue = {date.date(): 0 for date in date_range}

            # Get shop's products
            shop_products_query = select(ShopProduct).where(
                ShopProduct.shop_id == shop.shop_id
            )
            shop_products = await self.db.execute(shop_products_query)
            shop_products = shop_products.scalars().all()
            product_ids = [sp.product_id for sp in shop_products]

            # Get orders for shop's products
            orders_query = select(OrderItem).where(
                OrderItem.product_id.in_(product_ids),
                OrderItem.order_at >= start_of_month,
                OrderItem.order_at <= end_of_month,
            )
            orders = await self.db.execute(orders_query)
            orders = orders.scalars().all()

            # Calculate daily revenue
            for order in orders:
                product_query = select(Product).where(
                    Product.product_id == order.product_id
                )
                product = await self.db.execute(product_query)
                product = product.scalar_one_or_none()

                if product:
                    total_price = order.quantity * product.price
                    order_day = order.order_at.date()
                    daily_revenue[order_day] += total_price

            # Create visualization
            dates = list(daily_revenue.keys())
            revenues = [daily_revenue[date] for date in dates]

            fig = go.Figure()
            fig.add_trace(
                go.Scatter(
                    x=dates,
                    y=revenues,
                    mode="lines",
                    name="Revenue",
                    line=dict(color="#2E86C1", width=2),
                )
            )
            fig.update_layout(
                title=f"Daily Revenue for {shop.shop_name}",
                title_x=0.5,
                xaxis_title="Date",
                yaxis_title="Revenue ($)",
                plot_bgcolor="white",
                paper_bgcolor="white",
                font=dict(size=12),
                margin=dict(l=50, r=50, t=70, b=50),
                yaxis=dict(gridcolor="#E5E5E5", zerolinecolor="#E5E5E5"),
                xaxis=dict(gridcolor="#E5E5E5", zerolinecolor="#E5E5E5"),
            )

            chart_html = fig.to_html(full_html=False, config={"displaylogo": False})

            # Cache the result
            # self.redis.setex(cache_key, REDIS_TTL, chart_html)

            return HTMLResponse(content=chart_html)

        except Exception as e:
            logger.error(str(e))
            return HTMLResponse(
                content="<div>Error generating revenue statistics</div>",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    async def statistics_top_products(self, shop_data: ShopGetData, current_user: User):
        try:
            shop_query = select(Shop).where(Shop.owner_id == current_user.user_id)
            result = await self.db.execute(shop_query)
            shop = result.scalar_one_or_none()

            if not shop:
                return JSONResponse(
                    content={"Message": "Shop not found"},
                    status_code=status.HTTP_404_NOT_FOUND,
                )

            timestamp_dt = shop_data.timestamp
            cache_key = (
                f"shop:{shop.shop_id}:top_products:{timestamp_dt.strftime('%Y-%m')}"
            )


        
            year = timestamp_dt.year
            month = timestamp_dt.month
            start_of_month = datetime(year, month, 1)
            _, last_day = calendar.monthrange(year, month)
            end_of_month = datetime(year, month, last_day, 23, 59, 59)

          
            shop_products_query = select(ShopProduct).where(
                ShopProduct.shop_id == shop.shop_id
            )
            shop_products = await self.db.execute(shop_products_query)
            shop_products = shop_products.scalars().all()
            product_ids = [sp.product_id for sp in shop_products]

          
            product_sales = {}
            orders_query = select(OrderItem).where(
                OrderItem.product_id.in_(product_ids),
                OrderItem.order_at >= start_of_month,
                OrderItem.order_at <= end_of_month,
            )
            orders = await self.db.execute(orders_query)
            orders = orders.scalars().all()

            for order in orders:
                if order.product_id not in product_sales:
                    product_sales[order.product_id] = 0
                product_sales[order.product_id] += order.quantity

          
            products_data = []
            for product_id, sales in product_sales.items():
                product_query = select(Product).where(Product.product_id == product_id)
                product = await self.db.execute(product_query)
                product = product.scalar_one_or_none()
                if product:
                    products_data.append({"name": product.product_name, "sales": sales})

      
            products_data.sort(key=lambda x: x["sales"], reverse=True)
            top_products = products_data[:10]

            fig = go.Figure(
                data=[
                    go.Bar(
                        x=[p["name"] for p in top_products],
                        y=[p["sales"] for p in top_products],
                        marker_color="#3498DB",
                        text=[f"{p['sales']} units" for p in top_products],
                        textposition="auto",
                    )
                ]
            )
            fig.update_layout(
                title=f"Top Products by Sales for {shop.shop_name}",
                title_x=0.5,
                xaxis_title="Product Name",
                yaxis_title="Units Sold",
                plot_bgcolor="white",
                paper_bgcolor="white",
                font=dict(size=12),
                margin=dict(l=50, r=50, t=70, b=100),
                yaxis=dict(gridcolor="#E5E5E5", zerolinecolor="#E5E5E5"),
                xaxis=dict(tickangle=45, gridcolor="#E5E5E5", zerolinecolor="#E5E5E5"),
            )

            chart_html = fig.to_html(full_html=False, config={"displaylogo": False})
           

            return HTMLResponse(content=chart_html)

        except Exception as e:
            logger.error(str(e))
            return HTMLResponse(
                content="<div>Error generating top products statistics</div>",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    async def statistics_categories(self, shop_data: ShopGetData, current_user: User):
        try:
            shop_query = select(Shop).where(Shop.owner_id == current_user.user_id)
            result = await self.db.execute(shop_query)
            shop = result.scalar_one_or_none()

            if not shop:
                return JSONResponse(
                    content={"Message": "Shop not found"},
                    status_code=status.HTTP_404_NOT_FOUND,
                )

            timestamp_dt = shop_data.timestamp
            cache_key = (
                f"shop:{shop.shop_id}:category_stats:{timestamp_dt.strftime('%Y-%m')}"
            )

        
            year = timestamp_dt.year
            month = timestamp_dt.month
            start_of_month = datetime(year, month, 1)
            _, last_day = calendar.monthrange(year, month)
            end_of_month = datetime(year, month, last_day, 23, 59, 59)

         
            shop_products_query = select(ShopProduct).where(
                ShopProduct.shop_id == shop.shop_id
            )
            shop_products = await self.db.execute(shop_products_query)
            shop_products = shop_products.scalars().all()
            product_ids = [sp.product_id for sp in shop_products]

            get_all_categories_query = select(Category)
            all_categories = await self.db.execute(get_all_categories_query)
            all_categories = all_categories.scalars().all()

            category_sales = {}
            for cat in all_categories:
                category_sales[cat.cat_name.value] = 0

            for product_id in product_ids:
                cat_query = select(CategoryProduct).where(
                    CategoryProduct.product_id == product_id
                )
                cats = await self.db.execute(cat_query)
                cats = cats.scalars().all()

                for cat in cats:
                    cat_name_query = select(Category).where(
                        Category.cat_id == cat.cat_id
                    )
                    cat_result = await self.db.execute(cat_name_query)
                    category = cat_result.scalar_one_or_none()

                    if category:
                        if category.cat_name.value not in category_sales:
                            category_sales[category.cat_name.value] = 0
                            
                        orders_query = select(OrderItem).where(
                            OrderItem.product_id == product_id,
                            OrderItem.order_at >= start_of_month,
                            OrderItem.order_at <= end_of_month,
                        )
                        orders = await self.db.execute(orders_query)
                        orders = orders.scalars().all()

                        for order in orders:
                            category_sales[category.cat_name.value] += order.quantity

        
            fig = go.Figure(
                data=[
                    go.Bar(
                        x=list(category_sales.keys()),
                        y=list(category_sales.values()),
                        marker_color="#2ECC71",
                        text=[f"{sales} units" for sales in category_sales.values()],
                        textposition="auto",
                    )
                ]
            )
            fig.update_layout(
                title=f"Category Distribution for {shop.shop_name}",
                title_x=0.5,
                xaxis_title="Category",
                yaxis_title="Units Sold",
                plot_bgcolor="white",
                paper_bgcolor="white",
                font=dict(size=12),
                margin=dict(l=50, r=50, t=70, b=100),
                yaxis=dict(gridcolor="#E5E5E5", zerolinecolor="#E5E5E5"),
                xaxis=dict(tickangle=45, gridcolor="#E5E5E5", zerolinecolor="#E5E5E5"),
            )

            chart_html = fig.to_html(full_html=False, config={"displaylogo": False})

            return HTMLResponse(content=chart_html)

        except Exception as e:
            logger.error(str(e))
            return HTMLResponse(
                content="<div>Error generating category statistics</div>",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    async def get_sale_history(self, current_user: User):
        try:

            get_shop_query = select(Shop).where(Shop.owner_id == current_user.user_id)
            shop_result = await self.db.execute(get_shop_query)
            shop = shop_result.scalar_one_or_none()

            if not shop:
                return JSONResponse(
                    content={"Message": "Shop not found"},
                    status_code=status.HTTP_404_NOT_FOUND,
                )

            get_shop_product = select(ShopProduct).where(
                ShopProduct.shop_id == shop.shop_id
            )
            shop_products = await self.db.execute(get_shop_product)
            shop_products = shop_products.scalars().all()

            if not shop_products:
                return JSONResponse(
                    content={"Message": "No products found"},
                    status_code=status.HTTP_404_NOT_FOUND,
                )

            product_ids = [sp.product_id for sp in shop_products]

            get_order_items = (
                select(OrderItem)
                .where(OrderItem.product_id.in_(product_ids))
                .order_by(OrderItem.order_at.desc())
            )
            order_items = await self.db.execute(get_order_items)
            order_items = order_items.scalars().all()

            if not order_items:
                return JSONResponse(
                    content={"Message": "No sales history found"},
                    status_code=status.HTTP_404_NOT_FOUND,
                )

            orders_dict = {}
            for order_item in order_items:
                if order_item.order_id not in orders_dict:
                    orders_dict[order_item.order_id] = {
                        "order_id": str(order_item.order_id),
                        "created_at": str(order_item.order_at),
                        "products": [],
                        "total_amount": 0,
                    }

                get_product = select(Product).where(
                    Product.product_id == order_item.product_id
                )
                product = await self.db.execute(get_product)
                product = product.scalar_one_or_none()

                if product:
                    item_total = order_item.quantity * product.price
                    orders_dict[order_item.order_id]["products"].append(
                        {
                            "product_id": str(product.product_id),
                            "product_name": product.product_name,
                            "product_description": product.product_description,
                            "price": product.price,
                            "quantity": order_item.quantity,
                            "total": item_total,
                        }
                    )
                    orders_dict[order_item.order_id]["total_amount"] += item_total

            response = list(orders_dict.values())
            response.sort(key=lambda x: x["created_at"], reverse=True)

            return JSONResponse(content=response, status_code=status.HTTP_200_OK)

        except Exception as e:
            await self.db.rollback()
            logger.error(str(e))
            return JSONResponse(
                content={"Message": "Unexpected error"},
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
