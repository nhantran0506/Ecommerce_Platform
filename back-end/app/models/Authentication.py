from sqlalchemy import ForeignKey, UUID, Column, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship, mapped_column, Mapped
import uuid
from abc import abstractmethod
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from db_connector import Base
from models.Users import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Authentication(Base):
    __tablename__ = "authentication"

    user_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    user_name: Mapped[UUID] = mapped_column(
        String,
        ForeignKey("users.phone_number"),
        nullable=False,
        unique=True,
        index=True,
    )
    hash_pwd: Mapped[String] = Column(String, nullable=False)
    is_deleted: Mapped[Boolean] = Column(Boolean, default=False)

    user: Mapped["User"] = relationship(
        "User", back_populates="authenticate"
    )

    @staticmethod
    async def hash_password(password: str) -> str:
        return pwd_context.hash(password)

    def verify_password(self, password: str) -> bool:
        try:
            if not password:
                raise ValueError("Password is required.")
            return pwd_context.verify(password, self.hash_pwd)
        except Exception as e:
            raise e
