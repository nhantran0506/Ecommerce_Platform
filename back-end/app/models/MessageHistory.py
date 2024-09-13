from sqlalchemy import String, Column, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
import enum
from db_connector import Base
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from models.ChatHistory import ChatHistory
import uuid
from sqlalchemy.sql import func


class MessageRole(enum.Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class MessageHistory(Base):
    __tablename__ = "message_history"

    message_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(
        UUID(as_uuid=True), ForeignKey("chat_history.session_id"), nullable=False
    )
    content = Column(String)
    role = Column(Enum(MessageRole), nullable=False, default=MessageRole.ASSISTANT)
    timestamp = Column(DateTime, default=datetime.now())

    chat_history = relationship(
        "ChatHistory", back_populates="message_history", foreign_keys=[session_id]
    )

    def __init__(self, role: str, content: str, session_id: str):
        self.role = role
        self.content = content
        self.session_id = session_id
