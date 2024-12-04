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
from models.CategoryProduct import *
import uuid


class CatTypes(enum.Enum):
    SHIRT = "SHIRT"
    PANTS = "PANTS"
    SHOES = "SHOES"
    ACCESSORIES = "ACCESSORIES"
    ELECTRONICS = "ELECTRONICS"
    BOOKS = "BOOKS"
    SPORTS = "SPORTS"
    BEAUTY = "BEAUTY"
    HEALTH = "HEALTH"
    HOME = "HOME"
    TOYS = "TOYS"
    FOOD = "FOOD"




class Category(Base):
    __tablename__ = "categories"

    cat_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    cat_name: Mapped[String] = mapped_column(
        Enum(CatTypes), nullable=False, unique=True, default=CatTypes.SHIRT
    )

    cat_products: Mapped["CategoryProduct"] = relationship(
        "CategoryProduct", back_populates="category", cascade="all, delete-orphan"
    )
