from fastapi import APIRouter, status, Depends, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from serializers.AISerializer import *
from serializers.UserSearializers import *
from middlewares import token_config
from db_connector import get_db
from controllers.ChatBotController import ChatBotController
from controllers.EmbeddingController import EmbeddingController
from managers.WebSocketManagers import WebSocketManager
import logging
import json
from middlewares import token_config



logger = logging.getLogger(__name__)
router = APIRouter(prefix="/ai", tags=["ai"])

ws_manager = WebSocketManager()


@router.post("/body_estimate")
async def login(image, user):
    pass

@router.post("/embedding")
async def embedding(embedding_request : EmbeddingPayload ,
                    embedding_controller : EmbeddingController = Depends(),
                    current_user = Depends(token_config.get_current_user)
):
    try:
        await embedding_controller.embedding(embedding_request)
    except Exception:
        return JSONResponse(
            content={"Message": "Unexpected error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )




@router.websocket("/chatbot")
async def websocket_endpoint(
    websocket: WebSocket, current_user=Depends(token_config.get_current_user_ws), db = Depends(get_db)
):
    await websocket.accept()
    session_id = await ws_manager.add_websocket(
        current_user, websocket, ChatBotController("llama3.1", db)
    )

    payload = {
        "session_id": session_id,
    }

    await websocket.send_json(json.dumps(payload))

    try:
        while True:
            message = await websocket.receive_json()
            query = message.get("message")

            client_session_id = message.get("session_id")
            await ws_manager.llm_answer(query, client_session_id, current_user)

    except WebSocketDisconnect:
        logger.info(f"WebSocket connection closed for session: {session_id}")
        ws_manager.remove_websocket(session_id)
