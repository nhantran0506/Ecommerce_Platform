import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_PASS = str(os.getenv('DATABASE_PASS'))
DATABASE_NAME = str(os.getenv('DATABASE_NAME'))
PORT = str(int(os.getenv('PORT')))


SERECT_KEY=str(os.getenv('SERECT_KEY'))
ALGORITHM=str(os.getenv('ALGORITHM'))
EXPIRE_TOKEN_TIME=int(os.getenv('EXPIRE_TOKEN_TIME'))