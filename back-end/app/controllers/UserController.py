from sqlalchemy import select, update, insert
from sqlalchemy.orm import Session
from models.Users import User, UserRoles
from models.Authentication import Authentication
from serializers.UserSearializers import *
from middlewares.token_config import *
from fastapi.responses import JSONResponse
from sqlalchemy.dialects.postgresql import UUID
from fastapi import status, Header, HTTPException, Security, Depends
from helper_collections import UTILS, EMAIL_TEMPLATE
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

class UserController:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def login(self, user: UserLogin):
        try:
            auth = await authenticate_user(self.db, user.user_name, user.password)
            if not auth:
                return JSONResponse(
                    content={"Message": "Invalid username or password."},
                    status_code=status.HTTP_401_UNAUTHORIZED,
                )
            
            query = select(User).where(User.user_id == auth.user_id)
            result = await self.db.execute(query)
            user = result.scalar_one_or_none()

            if user and user.deleted_date:
                update_stmt = update(User).where(User.user_id == auth.user_id).values(deleted_date=None)
                await self.db.execute(update_stmt)
                await self.db.commit()

            access_token = create_access_token(data={"user_name": auth.user_name})
            return {"token": access_token, "type": "bearer"}
        except Exception as e:
            await self.db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    async def get_user_by_id(self, user_id: str):
        try:
            query = select(User).where(User.user_id == user_id)
            result = await self.db.execute(query)
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
        try:  
            query = select(Authentication).where(Authentication.user_name == user.phone_number)
            result = await self.db.execute(query)
            check_exist = result.scalar_one_or_none()
            
            if check_exist:
                return JSONResponse(
                    content={"Message": "Phone number already exists"}, status_code=status.HTTP_409_CONFLICT
                )
            
            user_insert = insert(User).values(
                first_name=user.first_name,
                last_name=user.last_name,
                email = user.email,
                phone_number=user.phone_number,
                address=user.address,
                dob=user.dob,
            )
            result = await self.db.execute(user_insert)
            user_id = result.inserted_primary_key[0]

            auth_insert = insert(Authentication).values(
                user_id=user_id,
                user_name=user.phone_number,
                hash_pwd= await Authentication.hash_password(user.password)
            )
            await self.db.execute(auth_insert)
            await self.db.commit()
            
            return JSONResponse(
                content={"Message": "User created successfully."}, status_code=status.HTTP_201_CREATED
            )
        except Exception as e:
            await self.db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    async def forgot_password(self, user_data: UserForgotPassword):
        # try:
        query = select(User).where(User.email == user_data.email)
        result = await self.db.execute(query)
        user = result.scalar_one_or_none()

        if user is None:
            return JSONResponse(
                content={"Message": "Unable to find any user."},
                status_code=status.HTTP_404_NOT_FOUND,
            )
        
        new_password = await  UTILS.random_password()

        email_body = EMAIL_TEMPLATE.FORGOT_PASSWORD_EMAIL_TEMPLATE.format(user_name = f"{user.first_name} {user.last_name}", new_password=new_password)
        

        new_hash_password = await Authentication.hash_password(new_password)
        user_auth_update_query = update(Authentication).where(Authentication.user_id == user.user_id).values(
            user_name = user.phone_number,
            hash_pwd = new_hash_password
        )
        await self.db.execute(user_auth_update_query)
        await self.db.commit()

        email_send_check = await UTILS.send_email(recipient_email=user.email, subject="[RESET PASSWORD]", body=email_body)
        if email_send_check:
            return JSONResponse(content={"Message" : "Email have been sent successfully!"}, status_code=status.HTTP_200_OK)
        
        return JSONResponse(content={"Message" : "Email have not been sent!."}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        # except Exception as e:
        #     await self.db.rollback()
        #     raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    async def delete_user(self, current_user: User):
        update_stmt = update(User).where(User.user_id == current_user.user_id).values(
            deleted_date=datetime.now()
        )
        await self.db.execute(update_stmt)
        await self.db.commit()
        
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
            await self.db.execute(update_stmt)
            await self.db.commit()

        return JSONResponse(
            content={"Message": "User updated successfully."},
            status_code=status.HTTP_200_OK
        )