from fastapi import FastAPI, HTTPException, Depends
from db_connector import engine, Base, SessionLocal
from typing import List, Annotated
from sqlalchemy.orm import Session
app = FastAPI()

Base.metadata.create_all(bind=engine) # create all tables in database

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]




