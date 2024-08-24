from db_connector import db_dependency
from sqlalchemy.orm import Session
from models.Users import User, UserLogin
from middlewares.token_config import *
from fastapi.responses import JSONResponse
from sqlalchemy.dialects.postgresql import UUID
from fastapi import status



class UserController():
    def __init__(self, db : Session = db_dependency):
        self.db = db
    
    async def login(self, user : UserLogin):
        user = authenticate_user(user.user_name, user.password)
        if user is None:
            return JSONResponse(content={"Message" : "Invalid username or password."}, status_code=status.HTTP_401_UNAUTHORIZED)
        access_token = create_access_token(data = {"user_name" : user.user_name})
        return {"access_token" : access_token, "token_type" : "bearer"}
    
    async def get_user_by_id(self, user_id : str):
        try:
            print("hehe")
            user = self.db.query(User).filter(User.id == user_id).first()
            if user:
                return JSONResponse(content=user.to_dict(), status_code= status.HTTP_200_OK)
            else:
                return  JSONResponse(content={"Message" : "Unable to find any user."}, status_code= status.HTTP_404_NOT_FOUND)
        except Exception as e:
            raise e
    

    
     