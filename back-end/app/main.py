from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from db_connector import engine, Base, SessionLocal
from routers import products


Base.metadata.create_all(bind=engine)  # create all tables in database

app = FastAPI()

# allow NextJS, ReactJS to bypass CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def connection_check():
    return {"message": "connect to server successfully!"}


app.include_router(products.router)
