from dotenv import load_dotenv
import os

load_dotenv(".env")

DATABASE_PASS = str(os.environ.get("DATABASE_PASS"))
DATABASE_NAME = str(os.environ.get("DATABASE_NAME"))
PORT = str(os.environ.get("PORT"))
