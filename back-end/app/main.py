from fastapi import FastAPI, HTTPException, Depends
from db_connector import engine, Base, SessionLocal

Base.metadata.create_all(bind=engine) # create all tables in database

app = FastAPI()








