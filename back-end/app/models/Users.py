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

class UserRoles(enum.Enum):
    USER = "USER"
    ADMIN = "ADMIN"
    SHOP_OWNER = "SHOP_OWNER"


class User(Base):
    __tablename__ = "users"

    user_id : Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name: Mapped[String] = mapped_column(String, nullable=False)
    last_name: Mapped[String] = mapped_column(String, nullable=False)
    phone_number: Mapped[String] = mapped_column(String, nullable=False, unique=True)
    address: Mapped[String] = mapped_column(String, nullable=False)
    dob : Mapped[String]= mapped_column(DateTime, nullable=False)
    email: Mapped[String] = mapped_column(String, nullable=True)
    role : Mapped[String]= mapped_column(Enum(UserRoles), nullable=False, default=UserRoles.USER)
    is_deleted : Mapped[Boolean]= mapped_column(Boolean, default=False)
    deleted_date : Mapped[UUID]= mapped_column(DateTime, nullable=True)

    chat_history: Mapped[list["ChatHistory"]] = relationship("ChatHistory", back_populates="user")
    shops : Mapped["Shop"]= relationship("Shop", back_populates="owner")
    authenticate: Mapped["Authentication"] = relationship("Authentication", back_populates="user")
    product_ratings : Mapped[list["ProductRating"]]= relationship("ProductRating", back_populates="user") 
    shop_ratings : Mapped[list["ShopRating"]]= relationship("ShopRating", back_populates="user")

    def __init__(self, first_name, last_name, phone_number, address, dob, email=None):
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.address = address
        self.dob = dob
        self.email = email
