from fastapi import WebSocket
from starlette.websockets import WebSocketState
from controllers.ChatBotController import ChatBotController
from models.Users import User
from models.ChatHistory import ChatHistory


class WebSocketManager:
    def __init__(self, max_clients: int = 100):
        self.activate_websocket: dict = dict()
        self.MAX_CLIENTS = max_clients

    async def add_websocket(
        self, current_user: User, websocket: WebSocket, llm: ChatBotController
    ):
        session_id = await llm.add_user(current_user)
        if len(self.activate_websocket) >= self.MAX_CLIENTS:
            raise Exception("Use queues are full.")

        if session_id not in self.activate_websocket.keys():
            self.activate_websocket[session_id] = {
                "websocket": websocket,
                "llm": llm,
            }

        return str(session_id)

    async def llm_answer(self, query: str, session_id: str):
        print(self.activate_websocket)
        llm = self.activate_websocket[session_id]["llm"]
        response = await llm.answer(query, session_id)
        await self.activate_websocket[session_id]["websocket"].send_text(response)

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
