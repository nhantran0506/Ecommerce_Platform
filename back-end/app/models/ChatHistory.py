from sqlalchemy import Boolean, String, Column, DateTime, ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped
import enum
from db_connector import Base
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
import uuid


class ChatHistory(Base):
    __tablename__ = "chat_history"

    session_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.user_id"),
        default=uuid.uuid4(),
        index=True,
    )
    model_name: Mapped[String] = mapped_column(String)

    user: Mapped["User"] = relationship("User", back_populates="chat_history")
    message_history: Mapped[list["MessageHistory"]] = relationship(
        "MessageHistory", back_populates="chat_history"
    )

    def __init__(self, user_id: str, model_name: str):
        self.user_id = user_id
        self.model_name = model_name
