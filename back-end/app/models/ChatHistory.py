from sqlalchemy import (
    Boolean,
    String,
    Column,
    DateTime,
    Enum,
    ForeignKey
)
from sqlalchemy.orm import relationship
import enum
from db_connector import Base
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
import uuid


class ChatHistory(Base):
    __tablename__ = "chat_history"
    
    session_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4())
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        primary_key=True,
        default=uuid.uuid4(),
    )
    at = Column(DateTime, nullable=False, default=datetime.now())
    content = Column(String)
    
    
    def __init__(self, user_id : uuid, content : str):
        self.user_id = user_id
        self.content = content
        
        self.user = relationship("User", back_populates="chat_history", foreign_keys=[user_id])
    