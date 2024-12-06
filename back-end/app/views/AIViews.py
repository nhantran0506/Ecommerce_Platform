from fastapi import APIRouter, status, Depends, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from serializers.AISerializer import *
from serializers.UserSearializers import *
from middlewares import token_config
from db_connector import get_db
from controllers.ChatBotController import ChatBotController
from controllers.EmbeddingController import EmbeddingController
import logging
import json
from middlewares import token_config



logger = logging.getLogger(__name__)
router = APIRouter(prefix="/ai", tags=["ai"])




@router.post("/chatbot")
async def chatbot(query_payload : QueryPayload, chat_controller : ChatBotController = Depends(), current_user = Depends(token_config.get_current_user)):
    try:
        return await chat_controller.answer(query_payload, current_user)
    except Exception as e:
        logger.error(e)
        return JSONResponse(
            content={"Message": "Unexpected error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )