from fastapi import APIRouter, status, Request, Depends, WebSocket, WebSocketDisconnect
from controllers.UserController import UserController
from fastapi.responses import JSONResponse
from models.Users import User
from serializers.UserSearializers import *
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Session
from middlewares import token_config
from db_connector import get_db
from controllers.ChatBotController import ChatBotController
from managers.WebSocketManagers import WebSocketManager
import logging
import uuid
from transformers import pipeline

# pipe = pipeline("depth-estimation", model="Intel/dpt-hybrid-midas")


logger = logging.getLogger(__name__)
router = APIRouter(prefix="/ai", tags=["ai"])

ws_manager = WebSocketManager()


@router.post("/body_estimate")
async def login(image, user):
    pass

@router.websocket("/chatbot")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    session_id = str(uuid.uuid4())
    
    
    await websocket.send_text(f"SESSION_ID:{session_id}")

    try:
        while True:
            message = await websocket.receive_json()
            print(type(message))
            query = message.get("message")

            client_session_id = message.get("session_id")
            ws_manager.add_websocket(client_session_id, websocket, ChatBotController("llama3.1"))
           
            await ws_manager.llm_answer(query, session_id)

    except WebSocketDisconnect:
        print(f"WebSocket connection closed for session: {session_id}")
        ws_manager.remove_websocket(session_id)


