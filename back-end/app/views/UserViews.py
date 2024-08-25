from fastapi import APIRouter, status, Request, Depends
from controllers.UserController import UserController
from fastapi.responses import JSONResponse
from models.Users import User
from serializers.UserSearializers import *
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Session
from db_connector import get_db
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/users", tags=["users"])


@router.get("/login")
async def login(user: UserLogin, user_controller : UserController = Depends()):
    try:
        return await user_controller.login(user)
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
async def get_user(user_id: str):
    user_controller = UserController(Depends(get_db))
    try:
        return await user_controller.get_user_by_id(user_id)
    except Exception as e:
        logger.error(str(e))
        return JSONResponse(
            content={"Message": "Unexpected error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

# @router.post("/update_user/{user_id}")
# async def update_user(user_id: int, request: User):
#     pass

@router.post("/delete_user")
async def delete_user(user_deleted : UserDelete, user_controller : UserController = Depends()):
    try:
        
        return await user_controller.delete_user_by_id(user_deleted)
    except Exception as e:
        logger.error(str(e))
        return JSONResponse(
            content={"Message": "Unexpected error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
