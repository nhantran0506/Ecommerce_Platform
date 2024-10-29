from fastapi import APIRouter, status, Request, Depends
from controllers.UserController import UserController
from fastapi.responses import JSONResponse
from models.Users import User
from serializers.UserSearializers import *
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Session
from middlewares import token_config
from db_connector import get_db
import logging
from fastapi.security import OAuth2PasswordRequestForm

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/users", tags=["users"])


@router.post("/login")
async def login(user: UserLogin, user_controller : UserController = Depends()):
    try:
        return await user_controller.login(user)
    except Exception as e:
        logger.error(str(e))
        return JSONResponse(
            content={"Message": "Unexpected error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.post("/login_google")
async def login_google(token: str, user_controller: UserController = Depends()):
    try:
        return await user_controller.login_google(token)
    except Exception as e:
        logger.error(str(e))
        return JSONResponse(
            content={"Message": "Unexpected error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.post("/signup")
async def signup(user : UserCreateSerializer, user_controller : UserController = Depends()):
    try:
        return await user_controller.signup(user)
    except Exception as e:
        logger.error(str(e))
        return JSONResponse(
            content={"Message": "Unexpected error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )



@router.get("/{user_id}")
async def get_user(user_id: str, user_controller : UserController = Depends()):
    try:
        return await user_controller.get_user_by_id(user_id)
    except Exception as e:
        logger.error(str(e))
        return JSONResponse(
            content={"Message": "Unexpected error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

@router.post("/update_user")
async def update_user(user_update: UserUpdate , user_controller : UserController = Depends() ,current_user = Depends(token_config.get_current_user)):
    try:
        return await user_controller.update_user(user_update, current_user=current_user)
    except Exception as e:
        logger.error(str(e))
        return JSONResponse(
            content={"Message": "Unexpected error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

@router.post("/delete_user")
async def delete_user(user_controller : UserController = Depends(), current_user = Depends(token_config.get_current_user)):
    try:
        
        return await user_controller.delete_user(current_user)
    except Exception as e:
        logger.error(str(e))
        return JSONResponse(
            content={"Message": "Unexpected error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.post("/forgot_password")
async def forgot_password(user_data : UserForgotPassword ,user_controller : UserController = Depends()):
    try:
        print(user_data.email)
        return await user_controller.forgot_password(user_data)
    except Exception as e:
        logger.error(str(e))
        return JSONResponse(
            content={"Message": "Unexpected error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

