from fastapi import FastAPI, HTTPException, Depends
from db_connector import engine, Base, SessionLocal
from middlewares.routing_config import RouteConfig
import views
import views.AIViews
import views.CartViews
import views.UserViews
import views.ProductViews
import views.ShopViews
import views.RecommedViews
import uvicorn
from tasks.UserTasks import UserTasks

Base.metadata.create_all(bind=engine)  # create all tables in database

user_tasks = UserTasks()

app = FastAPI()

routing = RouteConfig()

# allow NextJS, ReactJS to bypass CORS
routing.configure_fe_policy(app)
routing.routing_config(
    app,
    list_routing=[
        views.ProductViews.router,
        views.UserViews.router,
        views.ShopViews.router,
        views.AIViews.router,
        views.RecommedViews.router,
        views.CartViews.router,
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
