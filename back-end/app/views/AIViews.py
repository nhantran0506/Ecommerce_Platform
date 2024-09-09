from fastapi import APIRouter, status, Request, Depends, WebSocket
from controllers.UserController import UserController
from fastapi.responses import JSONResponse
from models.Users import User
from serializers.UserSearializers import *
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Session
from middlewares import token_config
from db_connector import get_db
import logging
from transformers import pipeline

# pipe = pipeline("depth-estimation", model="Intel/dpt-hybrid-midas")


logger = logging.getLogger(__name__)
router = APIRouter(prefix="/ai", tags=["ai"])




@router.post("/body_estimate")
async def login(image, user):
    pass

@router.websocket("/chatbot")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")

