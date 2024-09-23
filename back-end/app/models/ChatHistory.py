from sqlalchemy import Boolean, String, Column, DateTime, ForeignKey
from sqlalchemy.orm import relationship
import enum
from db_connector import Base
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
import uuid


class ChatHistory(Base):
    __tablename__ = "chat_history"

    session_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        default=uuid.uuid4(),
    )
    model_name = Column(String)

    user = relationship("User", back_populates="chat_history")
    message_history = relationship("MessageHistory", back_populates="chat_history")

    def __init__(self, user_id: str, model_name: str):
        self.user_id = user_id
        self.model_name = model_name
