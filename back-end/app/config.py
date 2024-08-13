from dotenv import load_dotenv
import os

load_dotenv(".env")

DATABASE_PASS = str(os.environ.get('DATABASE_PASS'))
DATABASE_NAME = str(os.environ.get('ecommerce_platform'))
PORT = str(os.environ.get('PORT'))