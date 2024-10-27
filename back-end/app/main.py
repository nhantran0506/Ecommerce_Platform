import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from fastapi import FastAPI, HTTPException, Depends
from db_connector import engine, Base
from middlewares.routing_config import RouteConfig
from authlib.integrations.starlette_client import OAuth
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

routing = RouteConfig()


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def startup_event():
    await create_tables()


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
