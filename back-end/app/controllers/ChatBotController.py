from sqlalchemy import insert, select
from models.MessageHistory import MessageHistory
from llama_index.core.llms import ChatMessage
from llama_index.llms.ollama import Ollama
from db_connector import get_db
from models.Users import User
from sqlalchemy.ext.asyncio import AsyncSession
from models.ChatHistory import ChatHistory
from models.MessageHistory import MessageRole
from .EmbeddingController import EmbeddingController
from llama_index.core import PromptTemplate
from helper_collections.PROMPTs import *
from typing import List
from fastapi import Depends
from sqlalchemy import func
from serializers.AISerializer import QueryPayload
from fastapi.responses import JSONResponse
from fastapi import status


class ChatBotController:
    embedding_engine = EmbeddingController()

    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.llm = Ollama("llama3.2", request_timeout=500)
        self.db = db

    async def add_user(self, user: User, model_name: str):
        try:
            insert_stmt = insert(ChatHistory).values(
                user_id=user.user_id, model_name=model_name
            )
            result = await self.db.execute(insert_stmt)
            await self.db.commit()
            return str(result.inserted_primary_key[0])
        except Exception as e:
            await self.db.rollback()
            raise e

    async def get_history(self, session_id: str):
        query = (
            select(MessageHistory)
            .where(MessageHistory.session_id == session_id)
            .order_by(MessageHistory.timestamp.desc())
        )
        result = await self.db.execute(query)
        history = result.scalars().all()

        return [
            ChatMessage(role=message.role, content=message.content)
            for message in history
        ]

    async def add_message(
        self, role: str, content: str, session_id: str
    ) -> MessageHistory:
        try:
            if session_id:
                insert_stmt = insert(MessageHistory).values(
                    role=role, content=content, session_id=session_id
                )
            else:
                insert_stmt = (
                    insert(MessageHistory)
                    .values(role=role, content=content)
                    .returning(MessageHistory)
                )
            result = await self.db.execute(insert_stmt)
            await self.db.commit()
            return result
        except Exception as e:
            await self.db.rollback()
            raise e

    def intent_detection(self, query):
        intent_prompt = PromptTemplate(INTENT_DETECTION).format(query=query)
        intent_output = self.llm.complete(prompt=intent_prompt).text

        return "query" if "query" in intent_output.lower() else intent_output

    async def answer(self, query_payload: QueryPayload, current_user: User):
        try:
            query = query_payload.query
            session_id = query_payload.session_id

            intent = self.intent_detection(query)

            llm_response = ""
            if intent == "query":
                nodes = self.embedding_engine.query(query, top_k=5, min_similarity=0.7)
                context = "".join(node["text"] for node in nodes)

                system_prompt = PromptTemplate(SYSTEM_PROMPT).format(
                    customer_name=f"{current_user.first_name} {current_user.last_name}",
                    customer_phone=current_user.phone_number,
                    customer_address=current_user.address,
                )

                default_prompt = PromptTemplate(DEFAULT_PROMPT).format(
                    context=context, user_query=query
                )

                chat_message = await self.add_message(
                    role=MessageRole.USER, content=default_prompt, session_id=session_id
                )
                session_id = chat_message.session_id

                system_msg = [ChatMessage(role=MessageRole.SYSTEM, content=system_prompt)]
                chat_history = await self.get_history(session_id)
                response = self.llm.chat(system_msg + chat_history)

                await self.add_message(
                    role=MessageRole.ASSISTANT,
                    content=response.message.content,
                    session_id=session_id,
                )
                llm_response = response.message.content
            else:
                intent = "search"
                llm_response = intent

            return JSONResponse(
                content={
                    "purpose": intent,
                    "session_id": session_id,
                    "response": llm_response,
                },
                status_code=status.HTTP_200_OK,
            )
        except Exception as e:
            await self.db.rollback()
            print(e)
            return JSONResponse(
                content={"Error": "Error with the server."},
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
