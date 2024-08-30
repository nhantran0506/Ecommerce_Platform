from sqlalchemy.orm import Session
from models.Users import User, UserRoles
from serializers.UserSearializers import *
from middlewares.token_config import *
from fastapi.responses import JSONResponse
from sqlalchemy.dialects.postgresql import UUID
from fastapi import status, Header, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


class UserController:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db
        

    async def login(self, user: UserLogin):
        user = authenticate_user(self.db, user.user_name, user.password)
        if not user:
            return JSONResponse(
                content={"Message": "Invalid username or password."},
                status_code=status.HTTP_401_UNAUTHORIZED,
            )
        access_token = create_access_token(data={"user_name": user.user_name})
        return {"Access Token": access_token, "Type": "bearer"}

    async def get_user_by_id(self, user_id: str):
        try:
            user = self.db.query(User).filter(User.id == user_id).first()
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
            user_id = user_parse.id,
            user_name = user_parse.phone_number,
            hash_pwd = data["password"]
        )


        self.db.add(auth)
        self.db.commit()
        self.db.refresh(auth) 
        return JSONResponse(
            content={"Message" : "User created successfully."}, status_code=status.HTTP_201_CREATED
        )

    async def delete_user_by_id(self,user_delte: UserDelete, role: str = Depends(get_user_role)):
        if role != 'ADMIN':
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You don't have power here.")
        
        user_id = user_delte.user_id
        
        auth_records = self.db.query(Authentication).filter(Authentication.user_id == user_id).all()
        for auth_record in auth_records:
            self.db.delete(auth_record)
        self.db.commit()
    
        user = self.db.query(User).filter(User.id == user_id).first()
        if user:
            self.db.delete(user)
            self.db.commit()
            return JSONResponse(
                content={"Message": "User deleted successfully."},
                status_code=status.HTTP_200_OK,
            )
        else:
            return JSONResponse(
                content={"Message": "Unable to find any user."},
                status_code=status.HTTP_404_NOT_FOUND,
            )






