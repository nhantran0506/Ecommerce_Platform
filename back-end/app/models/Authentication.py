from sqlalchemy import ForeignKey, UUID, Column, String, ForeignKey
from sqlalchemy.orm import relationship
import uuid
from abc import abstractmethod
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from db_connector import Base

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Authentication(Base):
    __tablename__ = "authentication"

    # id = ForeignKey("users.id")
    user_id = Column(UUID(as_uuid=True),ForeignKey("users.id"), primary_key=True, default=uuid.uuid4())
    user_name = Column(String, nullable=False, unique=True)
    hash_pwd = Column(String, nullable=False)

    user = relationship("User", back_populates="authenticate")

    @abstractmethod
    def get_user_by_username(db_connector : Session ,user_name : str):
        try:
            return db_connector.query(Authentication).filter(Authentication.user_name == user_name).first()
        except Exception as e:
            raise e

    def verify_password(self, password : str) -> bool:
        try:
            if not password:
                raise ValueError("Password is required.")
            return pwd_context.verify(password, self.hash_pwd.value)
        except Exception as e:
            raise e
