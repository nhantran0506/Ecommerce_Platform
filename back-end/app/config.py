import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_PASS = str(os.getenv('DATABASE_PASS'))
DATABASE_NAME = str(os.getenv('DATABASE_NAME'))
PORT = str(os.getenv('PORT'))


SERECT_KEY=str(os.getenv('SERECT_KEY'))
ALGORITHM=str(os.getenv('ALGORITHM'))
EXPIRE_TOKEN_TIME=int(str(os.getenv('EXPIRE_TOKEN_TIME')))

PORT_FE=str(os.getenv('PORT_FE'))
ADDRESS_FE=str(os.getenv('ADDRESS_FE'))


GMAIL_APP_PASSWORD = str(os.getenv('GMAIL_APP_PASS'))
SENDER_EMAIL = str(os.getenv('SENDER_EMAIL'))

GOOGLE_CLIENT_ID = str(os.getenv('GOOGLE_CLIENT_ID'))
GOOGLE_CLIENT_SECRET = str(os.getenv('GOOGLE_CLIENT_SECRET'))