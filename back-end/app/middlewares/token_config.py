from datetime import datetime, timedelta
from typing import Optional, Any
from jose import JWSError, jwt
from fastapi import HTTPException, status, Depends
from db_connector import get_db
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from models.Authentication import Authentication
from db_connector import db_dependency
from config import(
    ALGORITHM,
    SERECT_KEY,
    EXPIRE_TOKEN_TIME
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_access_token(data : dict, expires_delta : Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=EXPIRE_TOKEN_TIME)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SERECT_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(token: str = Depends(oauth2_scheme), db : Session = db_dependency):
    credentials_exceptions = HTTPException(
        status_code= status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers = {"WWW-Authenticate": "Bearer"}

    )
    try:
        payload = jwt.decode(token, SERECT_KEY, algorithms=[ALGORITHM])
        user_name : str = payload.get("user_name", None)
        if user_name is None:
            raise credentials_exceptions
    except:
        raise credentials_exceptions
    user = Authentication.get_user_by_username(db, user_name)
    if user is None:
        raise credentials_exceptions
    return user



def authenticate_user(user_name : str, password: str, db : Session = db_dependency):
    user = Authentication.get_user_by_username(db, user_name)
    if not user:
        return False
    if not user.verify_password(password):
        return False
    return user