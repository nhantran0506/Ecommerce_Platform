from sqlalchemy import String, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from db_connector import Base
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from llama_index.core.llms import MessageRole
import uuid
from sqlalchemy.sql import func


class MessageHistory(Base):
    __tablename__ = "message_history"

    message_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    session_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("chat_history.session_id"), nullable=False, index=True
    )
    content: Mapped[String] = mapped_column(String)
    role: Mapped[String] = mapped_column(
        Enum(MessageRole), nullable=False, default=MessageRole.ASSISTANT
    )
    timestamp: Mapped[DateTime] = mapped_column(DateTime, default=datetime.now())

    chat_history: Mapped["ChatHistory"] = relationship(
        "ChatHistory", back_populates="message_history"
    )

    def __init__(self, role: str, content: str, session_id: str):
        self.role = role
        self.content = content
        self.session_id = session_id
