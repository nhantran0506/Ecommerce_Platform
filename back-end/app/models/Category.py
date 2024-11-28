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
import enum


class CatTypes(enum.Enum):
    SHIRT = "SHIRT"


class Category(Base):
    __tablename__ = "categories"

    cat_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    cat_name: Mapped[str] = mapped_column(
        Enum(CatTypes, create_type=True, name="cattypes", values_callable=lambda obj: [e.value for e in obj]),
        nullable=False, unique=True
    )

    cat_products: Mapped["CategoryProduct"] = relationship(
        "CategoryProduct", back_populates="category", cascade="all, delete-orphan"
    )
