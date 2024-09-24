from sqlalchemy import select, update, insert
from sqlalchemy.orm import Session
from models.Users import User, UserRoles
from models.Authentication import Authentication
from serializers.UserSearializers import *
from middlewares.token_config import *
from fastapi.responses import JSONResponse
from sqlalchemy.dialects.postgresql import UUID
from fastapi import status, Header, HTTPException, Security, Depends
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
        
        query = select(User).where(User.user_id == auth.user_id)
        result = self.db.execute(query)
        user = result.scalar_one_or_none()

        if user and user.is_deleted:
            update_stmt = update(User).where(User.user_id == auth.user_id).values(is_deleted=False)
            self.db.execute(update_stmt)
            self.db.commit()

        access_token = create_access_token(data={"user_name": auth.user_name})
        return {"token": access_token, "type": "bearer"}

    async def get_user_by_id(self, user_id: str):
        try:
            query = select(User).where(User.user_id == user_id)
            result = self.db.execute(query)
            user = result.scalar_one_or_none()
            
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
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    async def signup(self, user: UserCreateSerializer):
        
        query = select(Authentication).where(Authentication.user_name == user.phone_number)
        result = self.db.execute(query)
        check_exist = result.scalar_one_or_none()
        
        if check_exist:
            return JSONResponse(
                content={"Message": "Phone number already exists"}, status_code=status.HTTP_409_CONFLICT
            )
        
        user_insert = insert(User).values(
            first_name=user.first_name,
            last_name=user.last_name,
            phone_number=user.phone_number,
            address=user.address,
            dob=user.dob,
        )
        result = self.db.execute(user_insert)
        user_id = result.inserted_primary_key[0]

        auth_insert = insert(Authentication).values(
            user_id=user_id,
            user_name=user.phone_number,
            hash_pwd=Authentication.hash_password(user.password)
        )
        self.db.execute(auth_insert)
        self.db.commit()
        
        return JSONResponse(
            content={"Message": "User created successfully."}, status_code=status.HTTP_201_CREATED
        )

    async def delete_user(self, current_user: User):
        update_stmt = update(User).where(User.user_id == current_user.user_id).values(
            is_deleted=True,
            deleted_date=datetime.now()
        )
        self.db.execute(update_stmt)
        self.db.commit()
        
        return JSONResponse(
            content="User deleted successfully.",
            status_code=status.HTTP_200_OK
        )

    async def update_user(self, user_update: UserUpdate, current_user: User):
        if not current_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

        update_values = {}
        for field, value in user_update.model_dump(exclude_unset=True).items():
            if value is not None:
                update_values[field] = value

        if update_values:
            update_stmt = update(User).where(User.user_id == current_user.user_id).values(**update_values)
            self.db.execute(update_stmt)
            self.db.commit()

        return JSONResponse(
            content={"Message": "User updated successfully."},
            status_code=status.HTTP_200_OK
        )