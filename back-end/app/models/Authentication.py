from sqlalchemy import ForeignKey, UUID, Column, String, ForeignKey
from sqlalchemy.orm import relationship
import uuid
from passlib.context import CryptContext
from db_connector import Base, SessionLocal

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# class Authentication(Base):
#     __tablename__ = "authentication"

#     id = ForeignKey("users.id")
#     user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"),default=str(uuid.uuid4()))
#     user_name = Column(String, nullable=False)
#     hash_pwd = Column(String, nullable=False)

#     user = relationship("User", back_populates="authenticate")

#     def get_user_id(self,db_connector : SessionLocal,user_name : str = None, passsword : str = None) -> str:
#         try:
#             return db_connector.query(Authentication).filter(Authentication.user_name == user_name).first()
#         except Exception as e:
#             raise e

#     def verify_password(self, password : str = None) -> bool:
#         try:
#             if not password:
#                 raise ValueError("Password is required.")
#             return pwd_context.verify_password(password, self.hash_pwd)
#         except Exception as e:
#             raise e
