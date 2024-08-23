from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from config import (
    PORT_FE,
    ADDRESS_FE
)

class RouteConfig:
    def __init__(self, port: str = PORT_FE, address : str = ADDRESS_FE) -> None:
        self.port = port
        self.address = address
    
    def configure_fe_policy(self, app: FastAPI) -> None:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[f"http://{self.address}:{self.port}"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    
    def routing_config(self, app : FastAPI, list_routing : list[APIRouter]) -> None:
        for route in list_routing:
            app.include_router(route)
