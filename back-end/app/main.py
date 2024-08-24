from fastapi import FastAPI, HTTPException, Depends
from db_connector import engine, Base, SessionLocal
from middlewares.routing_config import RouteConfig
import views
import views.UserViews
import views.products


Base.metadata.create_all(bind=engine)  # create all tables in database

app = FastAPI()

routing = RouteConfig()

# allow NextJS, ReactJS to bypass CORS
routing.configure_fe_policy(app)
routing.routing_config(app,
    list_routing=[
        views.products.router,
        views.UserViews.router,
    ]
)


@app.get("/")
def connection_check():
    return {"message": "connect to server successfully!"}



