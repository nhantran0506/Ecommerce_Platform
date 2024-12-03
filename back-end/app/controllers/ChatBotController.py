from sqlalchemy import select
from models.MessageHistory import MessageHistory
from llama_index.core.llms import ChatMessage, CompletionResponse, ChatResponse
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
from sqlalchemy.dialects.postgresql import insert
import logging
from bs4 import BeautifulSoup
import aiohttp
import re
import google.generativeai as genai
from config import (
    GOOGLE_STUDIO_API,
    MAX_NUM_CONNECTIONS,
    GOOGLE_CHAT_MODEL,
    OLLAMA_CHAT_MODEL,
)

logger = logging.getLogger(__name__)


class GoogleGemini:
    def __init__(
        self,
        model_name: str,
        temperature: int = 0.7,
        top_p: float = 0.95,
        top_k: float = 10,
        num_predict: int = 250,
    ):
        genai.configure(api_key=GOOGLE_STUDIO_API)
        generation_config = {
            "temperature": temperature,
            "top_p": top_p,
            "top_k": top_k,
            "max_output_tokens": num_predict,
            "response_mime_type": "text/plain",
        }

        self.model = genai.GenerativeModel(
            model_name=model_name,
            generation_config=generation_config,
        )

    def chat(self, chat_history: list[ChatMessage]):
        processes_history = []
        for chat_message in chat_history[:-1]:
            if chat_message.role == MessageRole.ASSISTANT:
                processes_history.append(
                    {
                        "role": "model",
                        "parts": [
                            chat_message.content + "\n",
                        ],
                    }
                )

            if chat_message.role == MessageRole.USER:
                processes_history.append(
                    {
                        "role": "user",
                        "parts": [
                            chat_message.content + "\n",
                        ],
                    }
                )

        chat_session = self.model.start_chat(history=processes_history)

        user_query = chat_history[-1].content
        response = chat_session.send_message(user_query)
        return ChatResponse(
            message=ChatMessage(
                role=MessageRole.ASSISTANT,
                content=response._result.candidates[0].content.parts[0].text,
            )
        )

    def complete(self, prompt: str):
        response = self.model.generate_content(prompt)
        return response


class ChatBotController:
    current_user_llm = []

    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.llm = GoogleGemini(model_name=GOOGLE_CHAT_MODEL, num_predict=250)
        self.name = GOOGLE_CHAT_MODEL
        self.db = db
        self.embedding_engine = EmbeddingController(self.db)

    async def get_page_content(self, html_url: str) -> str:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(html_url) as response:
                    if response.status != 200:
                        logger.error(
                            f"Error: Failed to fetch the page. Status code: {response.status}"
                        )
                        return ""

                    html_content = await response.text()

            soup = BeautifulSoup(html_content, "html.parser")
            body = soup.body
            if not body:
                logger.error("Error: No <body> tag found in the HTML.")
                return ""

            for element in body(["script", "style"]):
                element.decompose()

            text = body.get_text()

            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            clean_text = "\n".join(chunk for chunk in chunks if chunk)

            return clean_text
        except Exception as e:
            logger.error(f"Error: {str(e)}")
            return f"Page content not available right now."

    async def add_user(self, user: User, model_name: str):
        try:
            insert_stmt = (
                insert(ChatHistory)
                .values(user_id=user.user_id, model_name=model_name)
                .on_conflict_do_nothing()
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
        self,
        role: str,
        content: str,
        session_id: str,
        current_user: User,
        model_name: str,
    ) -> MessageHistory:
        try:

            session_id = await self.add_user(current_user, model_name)
            insert_stmt = insert(MessageHistory).values(
                role=role, content=content, session_id=session_id
            )
            await self.db.execute(insert_stmt)
            await self.db.commit()

            return session_id
        except Exception as e:
            logger.error(e)
            await self.db.rollback()
            raise e

    def intent_detection(self, query):
        intent_prompt = PromptTemplate(INTENT_DETECTION).format(query=query)
        intent_output = self.llm.complete(prompt=intent_prompt).text
        return "query" if "query" in intent_output.lower() else intent_output

    async def answer(self, query_payload: QueryPayload, current_user: User):
        try:
            # load baclancing
            self.current_user_llm.append(query_payload.session_id)
            if len(self.current_user_llm) > MAX_NUM_CONNECTIONS:
                self.llm = GoogleGemini(model_name=GOOGLE_CHAT_MODEL, num_predict=250)
                self.name = GOOGLE_CHAT_MODEL

            query = query_payload.query
            session_id = query_payload.session_id

            intent_check = self.intent_detection(query)
            intent = ""
            llm_response = ""
            if intent_check == "query":
                nodes = self.embedding_engine.query(query, top_k=5, min_similarity=0.7)
                context = "".join(node["text"] for node in nodes)

                system_prompt = PromptTemplate(SYSTEM_PROMPT).format(
                    customer_name=f"{current_user.first_name} {current_user.last_name}",
                    customer_phone=current_user.phone_number,
                    customer_address=current_user.address,
                    customer_email=current_user.email,
                )

                default_prompt = PromptTemplate(DEFAULT_PROMPT).format(
                    context=context,
                    user_query=query,
                    current_page_content=await self.get_page_content(
                        query_payload.current_route
                    ),
                )

                session_id = await self.add_message(
                    role=MessageRole.USER,
                    content=default_prompt,
                    session_id=session_id,
                    current_user=current_user,
                    model_name=self.name,
                )

                system_msg = [
                    ChatMessage(role=MessageRole.SYSTEM, content=system_prompt)
                ]
                chat_history = await self.get_history(session_id)
                response = self.llm.chat(system_msg + chat_history)

                session_id = await self.add_message(
                    role=MessageRole.ASSISTANT,
                    content=response.message.content,
                    session_id=session_id,
                    current_user=current_user,
                    model_name=self.name,
                )
                llm_response = response.message.content
            else:
                intent = "search"
                intent_check = intent_check.replace("SEARCH:", "")
                intent_check = intent_check.strip()
                llm_response = intent_check

            self.current_user_llm.pop()
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
            logger.error(e)
            return JSONResponse(
                content={"Error": "Error with the server."},
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
