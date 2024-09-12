from fastapi import WebSocket
from starlette.websockets import WebSocketState
from controllers.ChatBotController import ChatBotController

class WebSocketManager:
    def __init__(self):
        self.activate_websocket : dict[str : dict] = dict()
    
    def add_websocket(self, session_id: str ,websocket: WebSocket, llm : ChatBotController):
        if session_id not in self.activate_websocket.keys(): 
            self.activate_websocket[session_id] = {
                "websocket": websocket,
                "llm" : llm,
            }
    
    async def llm_answer(self, query : str, session_id: str):
        llm = self.activate_websocket[session_id]["llm"]
        response =await llm.answer(query, session_id)
        await self.activate_websocket[session_id]["websocket"].send_text(response)

    
    def broadcast_message(self, message: str):
        try:
            for _ , ws in self.activate_websocket.items():
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

    
