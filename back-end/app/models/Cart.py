from sqlalchemy import ForeignKey, UUID, Column, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship, mapped_column, Mapped
import uuid
from abc import abstractmethod
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from db_connector import Base
from models.Users import User


class Cart(Base):
    __tablename__ = 'cart'

    cart_id : Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, unique=True)
    user_id : Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.user_id"),nullable=False)
    