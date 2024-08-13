from sqlalchemy import Boolean, String, Integer, Column, ForeignKey
from db_connector import Base
from pydantic import BaseModel

class UserBase(BaseModel):
    id : int


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
