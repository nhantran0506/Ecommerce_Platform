from sqlalchemy import select, update, insert
from models.Authentication import Authentication
from serializers.UserSearializers import *
from middlewares.token_config import *
from fastapi.responses import JSONResponse
from fastapi import status, Header, HTTPException ,Depends
from helper_collections import UTILS, EMAIL_TEMPLATE
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from middlewares.oauth_config import verify_fb_oauth_token
from middlewares.token_config import authenticate_user
from passlib.context import CryptContext
import logging
import random

logger = logging.getLogger(__name__)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserController:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    # async def login_google(self, google_user):
    #     try:
    #         # google_user = await verify_google_oauth_token(code)
    #         email = google_user["email"]
    #         first_name = google_user.get("given_name")
    #         last_name = google_user.get("family_name")
    #         google_user_id = google_user["sub"]
    #         auth_query = select(Authentication).where(
    #             Authentication.user_name == email, Authentication.provider == "google"
    #         )
    #         result = await self.db.execute(auth_query)
    #         auth = result.scalar_one_or_none()
    #         if not auth:
    #             user_create_query = insert(User).values(
    #                 first_name=first_name,
    #                 last_name=last_name,
    #                 email=email,
    #                 phone_number=None,
    #                 address=None,
    #                 dob=None,
    #             )
    #             result = await self.db.execute(user_create_query)
    #             user_id = result.inserted_primary_key[0]
    #             auth_insert = insert(Authentication).values(
    #                 user_id=user_id,
    #                 user_name=email,
    #                 hash_pwd=None,
    #                 provider_user_id=google_user_id,
    #                 provider="google",
    #             )
    #             await self.db.execute(auth_insert)
    #             await self.db.commit()
    #         else:
    #             user_id = auth.user_id
    #         access_token = create_access_token(data={"user_name": email})

    #         response = JSONResponse({"message": "Login Successful"})
    #         response.set_cookie(
    #             key="access_token", value=access_token, httponly=True, secure=True
    #         )
    #         return response

    #     except ValueError as e:
    #         raise HTTPException(status_code=400, detail=str(e))
    #     except Exception as e:
    #         logger.error(f"Google login error: {str(e)}")
    #         raise HTTPException(status_code=500, detail=str(e))

    async def login_fb(self, code: str):
        try:
            fb_user = await verify_fb_oauth_token(code)
            name_parts = fb_user["name"].split()
            email = fb_user["email"]
            first_name = name_parts[0]
            last_name = name_parts[-1]
            google_user_id = fb_user["id"]
            auth_query = select(Authentication).where(
                Authentication.user_name == email, Authentication.provider == "facebook"
            )
            result = await self.db.execute(auth_query)
            auth = result.scalar_one_or_none()
            if not auth:
                user_create_query = insert(User).values(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    phone_number=None,
                    address=None,
                    dob=None,
                )
                result = await self.db.execute(user_create_query)
                user_id = result.inserted_primary_key[0]
                auth_insert = insert(Authentication).values(
                    user_id=user_id,
                    user_name=email,
                    hash_pwd=None,
                    provider_user_id=google_user_id,
                    provider="facebook",
                )
                await self.db.execute(auth_insert)
                await self.db.commit()
            else:
                user_id = auth.user_id
            access_token = create_access_token(data={"user_name": email})
            return {"token": access_token, "type": "bearer"}

        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid token")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

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
                update_stmt = (
                    update(User)
                    .where(User.user_id == auth.user_id)
                    .values(deleted_date=None)
                )
                await self.db.execute(update_stmt)
                await self.db.commit()

            access_token = create_access_token(data={"user_name": auth.user_name})
            return {"token": access_token, "type": "bearer"}
        except Exception as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )
    

    async def get_current_user(self, current_user : User):
        try:
            if not current_user:
                return JSONResponse(
                    content={"error" : "Invalid user"}, status_code=status.HTTP_401_UNAUTHORIZED
                )

            return current_user 
        except Exception as e:
            logger.error(str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )
    

    async def update_password(self, update_password: UserChangePasswordSerializer, current_user : User):
        try:
            query = select(Authentication).where(Authentication.user_name == current_user.email)
            result = await self.db.execute(query)
            user_auth = result.scalar_one_or_none()

            if not user_auth.verify_password(update_password.old_password):
                return JSONResponse(
                    content={"error": "User not found."},
                    status_code=status.HTTP_404_NOT_FOUND
                )
    
            auth_update = (
                update(Authentication)
                .where(Authentication.user_id == current_user.user_id)
                .values(hash_pwd=await Authentication.hash_password(update_password.new_password))
            )
            await self.db.execute(auth_update)
            await self.db.commit()

            return JSONResponse(
                content={"message": "Password updated successfully."},
                status_code=status.HTTP_200_OK
            )

        except Exception as e:
            await self.db.rollback()
            logger.error(str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )


    async def get_user_by_id(self, user_id: str):
        try:
            query = select(User).where(User.user_id == user_id)
            result = await self.db.execute(query)
            user = result.scalar_one_or_none()

            if not user:
                return JSONResponse(
                    content={"Message": "Unable to find any user."},
                    status_code=status.HTTP_404_NOT_FOUND,
                )
            
            response = {
                "first_name" : user.first_name,
                "last_name" : user.last_name,
            }

            return JSONResponse(
                    content=response, status_code=status.HTTP_200_OK
                )
                
        except Exception as e:
            logger.error(str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )

    async def signup(self, user: UserCreateSerializer):
        try:
            query = select(Authentication).where(Authentication.user_name == user.email)
            result = await self.db.execute(query)
            check_exist = result.scalar_one_or_none()

            if check_exist:
                return JSONResponse(
                    content={"Message": "Phone number already exists"},
                    status_code=status.HTTP_409_CONFLICT,
                )

            user_insert = insert(User).values(
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email,
                phone_number=user.phone_number,
                address=user.address,
                dob=user.dob,
            )
            result = await self.db.execute(user_insert)
            user_id = result.inserted_primary_key[0]

            auth_insert = insert(Authentication).values(
                user_id=user_id,
                user_name=user.email,
                hash_pwd=await Authentication.hash_password(user.password),
            )
            await self.db.execute(auth_insert)
            await self.db.commit()

            return JSONResponse(
                content={"Message": "User created successfully."},
                status_code=status.HTTP_201_CREATED,
            )
        except Exception as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )

    async def forgot_password(self, user_data: UserForgotPassword):
        query = select(Authentication).where(Authentication.user_name == user_data.email)
        result = await self.db.execute(query)
        auth = result.scalar_one_or_none()

        if auth is None:
            return JSONResponse(
                content={"Message": "Unable to find any user."},
                status_code=status.HTTP_404_NOT_FOUND,
            )

        # Generate a 6-digit temporary code
        temp_code = str(random.randint(100000, 999999))
        
        # Store the temp_code and its expiration time in the authentication record
        auth.temp_code = temp_code
        auth.temp_code_expiration = datetime.now() + timedelta(minutes=5)
        await self.db.commit()

        # Send the temporary code via email
        email_body = f"Your temporary code is: {temp_code}. It will expire in 5 minutes."
        await UTILS.send_email(user_data.email, "Password Reset Code", email_body)

        return JSONResponse(
            content={"Message": "Temporary code sent to your email."},
            status_code=status.HTTP_200_OK,
        )

    async def delete_user(self, current_user: User):
        update_stmt = (
            update(User)
            .where(User.user_id == current_user.user_id)
            .values(deleted_date=datetime.now())
        )
        await self.db.execute(update_stmt)
        await self.db.commit()

        return JSONResponse(
            content="User deleted successfully.", status_code=status.HTTP_200_OK
        )

    async def update_user(self, user_update: UserUpdate, current_user: User):
        try:
            if not current_user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
                )

            update_values = {}
            for field, value in user_update.model_dump(exclude_unset=True).items():
                if value is not None:
                    update_values[field] = value

            if update_values:
                update_stmt = (
                    update(User)
                    .where(User.user_id == current_user.user_id)
                    .values(**update_values)
                )
                await self.db.execute(update_stmt)
                await self.db.commit()

            return JSONResponse(
                content={"Message": "User updated successfully."},
                status_code=status.HTTP_200_OK,
            )
        except Exception as e:
            logger.error(str(e))
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )

    async def validate_temp_code(self, user_data: UserValidateCode):
        try:
            query = select(Authentication).where(Authentication.user_name == user_data.email)
            result = await self.db.execute(query)
            auth = result.scalar_one_or_none()

            if auth is None or auth.temp_code != user_data.temp_code:
                return JSONResponse(
                    content={"Message": "Invalid or expired temporary code."},
                    status_code=status.HTTP_400_BAD_REQUEST,
                )

            # Check if the code is expired
            if datetime.now() > auth.temp_code_expiration:
                return JSONResponse(
                    content={"Message": "Temporary code has expired."},
                    status_code=status.HTTP_400_BAD_REQUEST,
                )

            return JSONResponse(
                content={"Message": "Temporary code validated successfully."},
                status_code=status.HTTP_200_OK,
            )
        except Exception as e:
            await self.db.rollback()
            logger.error(str(e))
            return JSONResponse(content={"error:" : "INTERNAL_SERVER_ERROR"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    async def change_password_with_code(self, update_password: UserChangeNewPasswordSerializer, temp_code: str, user_email : str):
        try:
            query = select(Authentication).where(Authentication.user_name == user_email)
            result = await self.db.execute(query)
            auth = result.scalar_one_or_none()

            if auth is None or auth.temp_code != temp_code:
                return JSONResponse(
                    content={"Message": "Invalid or expired temporary code."},
                    status_code=status.HTTP_400_BAD_REQUEST,
                )

           
            if datetime.now() > auth.temp_code_expiration:
                return JSONResponse(
                    content={"Message": "Temporary code has expired."},
                    status_code=status.HTTP_400_BAD_REQUEST,
                )

           
            user_query = select(Authentication).where(Authentication.user_name == user_email)
            user_result = await self.db.execute(user_query)
            user = user_result.scalar_one_or_none()

            if user:
                user.hash_pwd = await Authentication.hash_password(update_password.new_password)
                auth.temp_code = None 
                auth.temp_code_expiration = None  
                await self.db.commit()

            return JSONResponse(
                content={"Message": "Password changed successfully."},
                status_code=status.HTTP_200_OK,
            )
        except Exception as e:
            await self.db.rollback()
            logger.error(str(e))
            return JSONResponse(content={"error:" : "INTERNAL_SERVER_ERROR"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
