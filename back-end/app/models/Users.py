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
import uuid


class UserRoles(enum.Enum):
    USER = "USER"
    ADMIN = "ADMIN"
    SHOP_OWNER = "SHOP_OWNER"


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False, unique=True)
    address = Column(String, nullable=False)
    dob = Column(DateTime, nullable=False)
    email = Column(String, nullable=True)
    role = Column(Enum(UserRoles), nullable=False, default=UserRoles.USER)
    is_deleted = Column(Boolean, default=False)
    deleted_date = Column(DateTime, nullable=True)

    chat_history = relationship("ChatHistory", back_populates="user")
    shops = relationship("Shop", back_populates="owner")

    shop_ratings = relationship("ShopRating", back_populates="user")
    product_ratings = relationship("ProductRating", back_populates="user")
    authenticate = relationship("Authentication", back_populates="user")

    def __init__(self, first_name, last_name, phone_number, address, dob, email=None):
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.address = address
        self.dob = dob
        self.email = email
