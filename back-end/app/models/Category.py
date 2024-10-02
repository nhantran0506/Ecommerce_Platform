from sqlalchemy import (
    Boolean,
    String,
    Column,
    DateTime,
    Enum,
)
from sqlalchemy.orm import relationship
import enum
from db_connector import Base
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.dialects.postgresql import UUID
from models.Ratings import *
import uuid


class Category(Base):
    __tablename__ = "categories"

    cat_id : Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cat_name : Mapped[String] = mapped_column(String, nullable= False, default="", unique=True)

    cat_products : Mapped["CategoryProduct"] = relationship("CategoryProduct", backref="category")
    user_interest: Mapped["UserInterest"] = relationship(
        "UserInterest", back_populates="category"
    )
    

    