from sqlalchemy import Boolean, String, Column, DateTime, Enum, Integer
from sqlalchemy.orm import relationship
import enum
from db_connector import Base
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.dialects.postgresql import UUID
from models.Ratings import *
from models.Cart import *
from models.Products import *
import uuid
from datetime import datetime


class InterestScore(enum.Enum):
    VIEW = 1
    CART = 3
    BUY = 5


class UserInterest(Base):
    __tablename__ = "user_interest"

    user_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.user_id"), primary_key=True, index=True
    )
    product_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("products.product_id"), primary_key=True
    )
    score: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime, default=datetime.now(), nullable=False
    )

    user: Mapped["User"] = relationship("User", back_populates="user_interest")
    product: Mapped["Product"] = relationship("Product", back_populates="interest")
