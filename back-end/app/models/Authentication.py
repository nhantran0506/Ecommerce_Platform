from sqlalchemy import ForeignKey, UUID, Column, String, ForeignKey
from sqlalchemy.orm import relationship
import uuid
from abc import abstractmethod
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from db_connector import Base
from models.Users import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Authentication(Base):
    __tablename__ = "authentication"

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        primary_key=True,
        default=uuid.uuid4(),
    )
    user_name = Column(
        String, ForeignKey("users.phone_number"), nullable=False, unique=True
    )
    hash_pwd = Column(String, nullable=False)

    

    def __init__(self, user_id, user_name, hash_pwd):
        self.user_id = user_id
        self.user_name = user_name
        self.hash_pwd = self.hash_password(hash_pwd)

        self.user = relationship("User", back_populates="authenticate", foreign_keys=[user_id])

    @abstractmethod
    def get_user_by_username(db_connector: Session, user_name: str):
        try:
            user =  db_connector.query(Authentication).filter(Authentication.user_name == user_name).first()
            user = db_connector.query(User).filter(User.id == user.user_id).first()
            return user
        except Exception as e:
            raise e

    @abstractmethod
    def hash_password(self, password: str) -> str:
        return pwd_context.hash(password)

    def verify_password(self, password: str) -> bool:
        try:
            if not password:
                raise ValueError("Password is required.")
            return pwd_context.verify(password, self.hash_pwd)
        except Exception as e:
            raise e
