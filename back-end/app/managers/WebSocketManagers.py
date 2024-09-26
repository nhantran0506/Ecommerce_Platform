from fastapi import WebSocket
from starlette.websockets import WebSocketState
from controllers.ChatBotController import ChatBotController
from models.Users import User
from models.ChatHistory import ChatHistory
import json


class WebSocketManager:
    def __init__(self, max_clients: int = 100):
        self.activate_websocket: dict = dict()
        self.MAX_CLIENTS = max_clients

    async def add_websocket(
        self, current_user: User, websocket: WebSocket, llm: ChatBotController
    ):
        if len(self.activate_websocket) >= self.MAX_CLIENTS:
            raise Exception("Use queues are full.")
        session_id = await llm.add_user(current_user)

        if session_id not in self.activate_websocket.keys():
            self.activate_websocket[session_id] = {
                "websocket": websocket,
                "llm": llm,
            }

        return str(session_id)

    async def llm_answer(self, query: str, session_id: str, current_user):
        llm = self.activate_websocket[session_id]["llm"]
        response, purpose = await llm.answer(query, session_id, current_user)

        payload = {
            "session_id": session_id,
            "purpose": purpose,
            "message": response,
        }

        await self.activate_websocket[session_id]["websocket"].send_json(
            json.dumps(payload)
        )

    def broadcast_message(self, message: str):
        try:
            for _, ws in self.activate_websocket.items():
                if ws["websocket"].client_state == WebSocketState.CONNECTING:
                    ws["websocket"].send_text(message)
        except Exception as e:
            return False

        return True

    def remove_websocket(self, session_id: str):
        if session_id in self.activate_websocket.keys():
            del self.activate_websocket[session_id]["websocket"]
            return True
        return False
