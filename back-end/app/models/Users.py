from sqlalchemy import Boolean, String, Integer, Column, ForeignKey, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
import enum
from db_connector import Base
from pydantic import BaseModel
from sqlalchemy.dialects.postgresql import UUID
import uuid



class UserBase(BaseModel):
    id : str
    first_name : str
    last_name : str
    address : str
    dob : DateTime
    email : str
    is_deleted : bool


class UserRoles(enum.Enum):
    USER = "USER"
    ADMIN = "ADMIN"
    SHOP_OWNER = "SHOP_OWNER"


class User(Base):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid = True), primary_key=True, default=str(uuid.uuid4()))
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    dob = Column(DateTime, nullable=False)
    email = Column(String, nullable=True)
    role = Column(Enum(UserRoles), nullable=False, default=UserRoles.USER)
    is_deleted = Column(Boolean, default=False)

    authenticate = relationship("Authentication", back_populates="user")

    
    
    