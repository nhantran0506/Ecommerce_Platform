from fastapi import APIRouter, status, Request
from controllers.UserController import UserController
from fastapi.responses import JSONResponse
from models.Users import User, UserBase, UserLogin
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Session
from db_connector import db_dependency

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/login")
async def login(user : UserLogin):
    try:
        user_controller = UserController()
        return await user_controller.login(user)
    except Exception as e:
        return JSONResponse(content={"message": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)




@router.get("/{user_id}")
async def get_user(user_id: str):
    user_controller = UserController()
    try:
        return await user_controller.get_user_by_id(user_id)
    except Exception as e:
        return JSONResponse(content={"message": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


# @router.post("/add_user")
# async def add_user(request: User):
#     pass


# @router.post("/update_user/{user_id}")
# async def update_user(user_id: int, request: User):
#     pass

# @router.post("/delete_user/{user_id}")
# async def delete_user(user_id: int):
#     passc


