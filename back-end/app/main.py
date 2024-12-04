import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from fastapi import FastAPI, HTTPException, Depends
from db_connector import engine, Base
from middlewares.routing_config import RouteConfig
from authlib.integrations.starlette_client import OAuth, OAuthError
import views
import views.AIViews
import views.AdminViews
import views.CartViews
import views.OrderViews
import views.UserViews
import views.ProductViews
import views.ShopViews
import views.RecommedViews
import uvicorn
from tasks.UserTasks import UserTasks
from config import DATABASE_PASS, DATABASE_NAME, PORT
from contextlib import asynccontextmanager
from starlette.middleware.sessions import SessionMiddleware
from models.Category import Category, CatTypes
from sqlalchemy import func, select
from sqlalchemy.dialects.postgresql import insert
from db_connector import get_db
from config import (
    SERECT_KEY,
    GOOGLE_CLIENT_ID,
    GOOGLE_CLIENT_SECRET,
)

routing = RouteConfig()

async def insert_default_enum_values(session: AsyncSession):
    async with session.begin():
        for cat_type in CatTypes:
            insert_cat_query = insert(Category).values(
                cat_name = cat_type.value
            ).on_conflict_do_update(
                index_elements=["cat_name"],
                set_={"cat_name": Category.cat_name},
            )
            await session.execute(insert_cat_query)
        await session.commit()

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    
    async for session in get_db():
        await insert_default_enum_values(session)


async def startup_event():
    await create_tables()


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     await create_tables()
#     yield
#     for route in app.routes:
#         if hasattr(route, "dependencies"):
#             for dep in route.dependencies:
#                 if hasattr(dep, "client"):
#                     dep.client.close()




user_tasks = UserTasks()

app = FastAPI()

app.add_event_handler("startup", startup_event)


routing.configure_middleware(app=app)
routing.routing_config(
    app,
    list_routing=[
        views.ProductViews.router,
        views.UserViews.router,
        views.ShopViews.router,
        views.AIViews.router,
        views.RecommedViews.router,
        views.CartViews.router,
        views.OrderViews.router,
        views.AdminViews.router,
    ],
)


@app.get("/")
def connection_check():
    return {"message": "connect to server successfully!"}



if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        # ssl_keyfile="key.pem",
        # ssl_certfile="cert.pem"
    )
