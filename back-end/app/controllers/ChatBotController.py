from models.MessageHistory import MessageHistory
from llama_index.core.llms import ChatMessage
from llama_index.llms.ollama import Ollama
from db_connector import SessionLocal, get_db
from models.Users import User
from sqlalchemy.orm import Session
from models.ChatHistory import ChatHistory
from models.MessageHistory import MessageRole
from .EmbeddingController import EmbeddingController
from llama_index.core import PromptTemplate
from helper_collections.PROMPTs import *
from typing import List
from .EmbeddingController import EmbeddingController
from fastapi import Depends

class ChatBotController:
    embedding_engine = EmbeddingController()
    
    
    def __init__(self, model_name: str, db: Session = Depends(get_db)):
        self.llm = Ollama(model_name, request_timeout=500)
        self.db = db

    async def add_user(self, user: User):
        self.db = SessionLocal()
        try:
            chat_history = ChatHistory(user.id, "llama3.1")
            self.db.add(chat_history)
            self.db.commit()
            self.db.refresh(chat_history)
            return str(chat_history.session_id)
        except Exception as e:
            self.db.rollback()
            raise e

    async def get_history(self, session_id: str):
        self.db = SessionLocal()
        history = (
            self.db.query(MessageHistory)
            .filter(MessageHistory.session_id == session_id)
            .order_by(MessageHistory.timestamp.desc())
            .all()
        )

        result = []
        for message in history or []:
            result.append(ChatMessage(role=message.role, content=message.content))

        return result

    async def add_message(self, role: str, content: str, session_id: str):
        self.db = SessionLocal()
        try:
            message = MessageHistory(role=role, content=content, session_id=session_id)
            self.db.add(message)
            self.db.commit()
            self.db.refresh(message)
        except Exception as e:
            self.db.rollback()
            raise e

    def intent_detection(self, query):
        intent_prompt = PromptTemplate(INTENT_DETECTION).format(query=query)
        intent_output = self.llm.complete(prompt=intent_prompt).text

        if "query" in intent_output.lower():
            return "query"

        return intent_output

    async def answer(self, query: str, session_id: str, current_user: User):

        intent = self.intent_detection(query)

        # query
        if intent == "query":
            nodes = self.embedding_engine.query(query)

            context = ""
            for node in nodes:
                context += node["text"]

            system_prompt = PromptTemplate(SYSTEM_PROMPT).format(
                customer_name=f"{current_user.first_name} {current_user.last_name}",
                customer_phone=current_user.phone_number,
                customer_address=current_user.address,
            )

            default_prompt = PromptTemplate(DEFAULT_PROMPT).format(context=context)

            await self.add_message(
                role=MessageRole.USER, content=default_prompt, session_id=session_id
            )

            system_msg = [ChatMessage(role=MessageRole.SYSTEM, content=system_prompt)]
            chat_hisory = await self.get_history(session_id)
            reponse = self.llm.chat(system_msg + chat_hisory)

            await self.add_message(
                role=MessageRole.ASSISTANT,
                content=reponse.message.content,
                session_id=session_id,
            )

            return reponse.message.content, intent

        return intent, "search"
