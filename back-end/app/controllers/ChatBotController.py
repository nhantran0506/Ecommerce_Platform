from  models_collection import MODELS
from models.MessageHistory import MessageHistory
from llama_index.core.llms import ChatMessage
from llama_index.llms.ollama import Ollama
from db_connector import SessionLocal
from models.Users import User
from models.ChatHistory import ChatHistory
from models.MessageHistory import MessageRole


class ChatBotController():
    def __init__(self, model_name: str):
        self.llm =  Ollama(model_name, request_timeout=500) # MODELS.get_model(model_name)
    
    async def add_user(self, user : User):
        db = SessionLocal()
        try:
            chat_history = ChatHistory(user.id, "llama3.1")
            db.add(chat_history)
            db.commit()
            db.refresh(chat_history)
            return str(chat_history.session_id)
        except Exception as e:
            db.rollback()
            raise e
    
    async def get_history(self, session_id : str):
        db = SessionLocal()
        history = db.query(MessageHistory).filter(MessageHistory.session_id == session_id).order_by(MessageHistory.timestamp.desc()).all()

        result = []
        for message in history or []:
            result.append(
                ChatMessage(role=message.role, content=message.content)       
            )
        
        return result

    async def add_message(self, role : str, content : str ,session_id : str):
        db = SessionLocal()
        try:
            message = MessageHistory(role=role, content=content, session_id=session_id)
            db.add(message)
            db.commit()
            db.refresh(message)
        except Exception as e:
            db.rollback()
            raise e
        
        
    async def answer(self, query : str, session_id : str):
        
        await self.add_message(role=MessageRole.USER, content=query, session_id=session_id)

        chat_hisory = await self.get_history(session_id)

        # chat_hisory += [ChatMessage(role="user", content=query)]

        reponse = self.llm.chat(chat_hisory)

        
        await self.add_message(role=MessageRole.ASSISTANT, content=reponse.message.content, session_id=session_id)
        
        return reponse.message.content





