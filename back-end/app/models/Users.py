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
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column, Mapped
import uuid


class UserRoles(enum.Enum):
    USER = "USER"
    ADMIN = "ADMIN"
    SHOP_OWNER = "SHOP_OWNER"


class User(Base):
    __tablename__ = "users"

    user_id : Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name : Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)
    phone_number: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    address: Mapped[str] = mapped_column(String, nullable=False)
    dob: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=True)
    role: Mapped[str] = mapped_column(Enum(UserRoles), nullable=False, default=UserRoles.USER)
    is_deleted : Mapped[Boolean]= mapped_column(Boolean, default=False)
    deleted_date : Mapped[DateTime]= mapped_column(DateTime, nullable=True)
    
    
    

    chat_history : Mapped["ChatHistory"] = relationship("ChatHistory", back_populates="user")
    shops : Mapped["Shop"] = relationship("Shop", back_populates="owner")
    shop_ratings : Mapped["ShopRating"] = relationship("ShopRating", back_populates="user")
    product_ratings : Mapped["ProductRating"] = relationship("ProductRating", back_populates="user")
    authenticate : Mapped["Authentication"] = relationship("Authentication", back_populates="user")

    def __init__(self, first_name, last_name, phone_number, address, dob, email=None):
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.address = address
        self.dob = dob
        self.email = email
