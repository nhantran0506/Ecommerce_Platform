from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from config import PORT_FE, ADDRESS_FE
from authlib.integrations.starlette_client import OAuth
from starlette.middleware.sessions import SessionMiddleware
from config import (
    SERECT_KEY,
    GOOGLE_CLIENT_ID,
    GOOGLE_CLIENT_SECRET,
)


class RouteConfig:
    def __init__(self, port: str = PORT_FE, address: str = ADDRESS_FE) -> None:
        self.port = port
        self.address = address
        

    def configure_middleware(self, app: FastAPI) -> None:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"], #allow_origins=[f"http://{self.address}:{self.port}/"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        app.add_middleware(
            SessionMiddleware,
            secret_key = SERECT_KEY,
        )


    def routing_config(self, app: FastAPI, list_routing: list[APIRouter]) -> None:
        for route in list_routing:
            app.include_router(route)
