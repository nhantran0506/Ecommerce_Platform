from sqlalchemy import insert, select
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
from fastapi import Depends
from sqlalchemy import func

class ChatBotController:
    embedding_engine = EmbeddingController()
    
    def __init__(self, model_name: str):
        self.llm = Ollama(model_name, request_timeout=500)
        self.db : Session = SessionLocal()

    async def add_user(self, user: User):
        try:
            insert_stmt = insert(ChatHistory).values(
                user_id=user.user_id, 
                model_name="llama3.1")
            result = self.db.execute(insert_stmt)
            self.db.commit()
            return str(result.inserted_primary_key[0])
        except Exception as e:
            self.db.rollback()
            raise e

    async def get_history(self, session_id: str):
        query = (
            select(MessageHistory)
            .where(MessageHistory.session_id == session_id)
            .order_by(MessageHistory.timestamp.desc())
        )
        result = self.db.execute(query)
        history = result.scalars()

        return [
            ChatMessage(role=message.role, content=message.content)
            for message in history
        ]

    async def add_message(self, role: str, content: str, session_id: str):
        try:
            insert_stmt = insert(MessageHistory).values(
                role=role, content=content, session_id=session_id
            )
            self.db.execute(insert_stmt)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise e

    def intent_detection(self, query):
        intent_prompt = PromptTemplate(INTENT_DETECTION).format(query=query)
        intent_output = self.llm.complete(prompt=intent_prompt).text

        return "query" if "query" in intent_output.lower() else intent_output

    async def answer(self, query: str, session_id: str, current_user: User):
        intent = self.intent_detection(query)

        if intent == "query":
            nodes = self.embedding_engine.query(query, top_k=5, min_similarity=0.7)
            context = "".join(node["text"] for node in nodes)

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
            chat_history = await self.get_history(session_id)
            response = self.llm.chat(system_msg + chat_history)

            await self.add_message(
                role=MessageRole.ASSISTANT,
                content=response.message.content,
                session_id=session_id,
            )

            return response.message.content, intent

        return intent, "search"