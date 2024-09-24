from sqlalchemy.orm import Session
from models.Users import User, UserRoles
from models.Authentication import Authentication
from serializers.UserSearializers import *
from middlewares.token_config import *
from fastapi.responses import JSONResponse
from sqlalchemy.dialects.postgresql import UUID
from fastapi import status, Header, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime


class UserController:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db
        

    async def login(self, user: UserLogin):
        auth = await authenticate_user(self.db, user.user_name, user.password)
        if not auth:
            return JSONResponse(
                content={"Message": "Invalid username or password."},
                status_code=status.HTTP_401_UNAUTHORIZED,
            )
        user = self.db.query(User).filter(User.user_id == auth.user_id).first()

        user.is_deleted = False
        self.db.commit()
        self.db.refresh(user)

        access_token = create_access_token(data={"user_name": auth.user_name})
        return {"token": access_token, "type": "bearer"}

    async def get_user_by_id(self, user_id: str):
        try:
            user = self.db.query(User).filter(User.user_id == user_id).first()
            if user:
                return JSONResponse(
                    content=user.to_dict(), status_code=status.HTTP_200_OK
                )
            else:
                return JSONResponse(
                    content={"Message": "Unable to find any user."},
                    status_code=status.HTTP_404_NOT_FOUND,
                )
        except Exception as e:
            raise e
        
    async def signup(self, user : UserCreateSerializer):
        data = user.model_dump(by_alias=True)
        
        check_exist = self.db.query(Authentication).filter(Authentication.user_name == data["phone_number"]).first()
        if check_exist:
            return JSONResponse(
                content={"Message" : "Phone number already exist"}, status_code=status.HTTP_409_CONFLICT
        )
        
        user_parse = User(
            first_name=data["first_name"],
            last_name=data["last_name"],
            phone_number=data["phone_number"],
            address=data["address"],
            dob=data["dob"],
        )
        
        self.db.add(user_parse)
        self.db.commit()
        self.db.refresh(user_parse) 


        auth = Authentication(
            user_id = user_parse.user_id,
            user_name = user_parse.phone_number,
            hash_pwd = data["password"]
        )


        self.db.add(auth)
        self.db.commit()
        self.db.refresh(auth) 
        return JSONResponse(
            content={"Message" : "User created successfully."}, status_code=status.HTTP_201_CREATED
        )
    
    async def delete_user(self, current_user : User):
        current_user.is_deleted = True
        current_user.deleted_date = datetime.now()
        self.db.commit()
        self.db.refresh(current_user)
        return JSONResponse(
            content="User deleted successfully.",
            status_code=status.HTTP_200_OK
        )
    

    # async def delete_user_by_id(self,user_delte: UserDelete, role: str):
    #     if role != UserRoles.ADMIN:
    #         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You don't have power here.")
        
    #     user_id = user_delte.user_id
        
    #     auth_records = self.db.query(Authentication).filter(Authentication.user_id == user_id).all()
    #     for auth_record in auth_records:
    #         self.db.delete(auth_record)
    #     self.db.commit()
    
    #     user = self.db.query(User).filter(User.id == user_id).first()
    #     if user:
    #         self.db.delete(user)
    #         self.db.commit()
    #         return JSONResponse(
    #             content={"Message": "User deleted successfully."},
    #             status_code=status.HTTP_200_OK,
    #         )
    #     else:
    #         return JSONResponse(
    #             content={"Message": "Unable to find any user."},
    #             status_code=status.HTTP_404_NOT_FOUND,
    #         )
    
    async def update_user(self, user_update: UserUpdate, current_user):
        if not current_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

        if user_update.first_name is not None:
            current_user.first_name = user_update.first_name
        if user_update.last_name is not None:
            current_user.last_name = user_update.last_name
        if user_update.phone_number is not None:
            current_user.phone_number = user_update.phone_number
        if user_update.address is not None:
            current_user.address = user_update.address
        if user_update.email is not None:
            current_user.email = user_update.email
        if user_update.dob is not None:
            current_user.dob = user_update.dob

        self.db.commit()
        self.db.refresh(current_user)  

        return JSONResponse(
            content={"Message": "User updated successfully."},
            status_code=status.HTTP_200_OK
        )

        


    







