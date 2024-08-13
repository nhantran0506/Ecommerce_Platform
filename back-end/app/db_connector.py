from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from typing import List, Annotated
from sqlalchemy.orm import Session
from fastapi import Depends
from config import (
    DATABASE_PASS,
    DATABASE_NAME,
    PORT
)


URL_DATABASE = f'postgresql://postgres:{DATABASE_PASS}!@localhost:{PORT}/{DATABASE_NAME}'

engine = create_engine(URL_DATABASE)

SessionLocal = sessionmaker(auto_commit=False, auto_flush=False, bind = engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]