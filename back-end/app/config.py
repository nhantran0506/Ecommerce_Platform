import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_PASS = str(os.getenv("DATABASE_PASS"))
DATABASE_NAME = str(os.getenv("DATABASE_NAME"))
PORT = str(os.getenv("PORT"))


SERECT_KEY = str(os.getenv("SERECT_KEY"))
ALGORITHM = str(os.getenv("ALGORITHM"))
EXPIRE_TOKEN_TIME = int(str(os.getenv("EXPIRE_TOKEN_TIME")))

PORT_FE = str(os.getenv("PORT_FE"))
ADDRESS_FE = str(os.getenv("ADDRESS_FE"))


GMAIL_APP_PASSWORD = str(os.getenv("GMAIL_APP_PASS"))
SENDER_EMAIL = str(os.getenv("SENDER_EMAIL"))

GOOGLE_CLIENT_ID = str(os.getenv("GOOGLE_CLIENT_ID"))
GOOGLE_CLIENT_SECRET = str(os.getenv("GOOGLE_CLIENT_SECRET"))
GOOGLE_REDIRECT_URI = str(os.getenv("GOOGLE_REDIRECT_URI"))

FACEBOOK_CLIENT_ID = str(os.getenv("FACEBOOK_CLIENT_ID"))
FACEBOOK_REDIRECT_URI = str(os.getenv("FACEBOOK_REDIRECT_URI"))
FACEBOOK_CLIENT_SECRET = str(os.getenv("FACEBOOK_CLIENT_SECRET"))

OLLAMA_CHAT_MODEL = str(os.getenv("OLLAMA_CHAT_MODEL"))
OLLAMA_EMBEDDING_MODEL = str(os.getenv("OLLAMA_EMBEDDING_MODEL"))
GOOGLE_CHAT_MODEL = str(os.getenv("GOOGLE_CHAT_MODEL"))
OLLAMA_BASE_URL = str(os.getenv("OLLAMA_BASE_URL"))
VECTOR_DIMENSIONS = int(os.getenv("VECTOR_DIMENSIONS"))
WEAVIATE_URL = str(os.getenv("WEAVIATE_URL"))

CDN_SERVER_URL = str(os.getenv("CDN_SERVER_URL"))
CDN_UPLOAD_URL = str(os.getenv("CDN_UPLOAD_URL"))
CDN_GET_URL = str(os.getenv("CDN_GET_URL"))
CDN_DELETE_URL = str(os.getenv("CDN_DELETE_URL"))

GOOGLE_STUDIO_API = str(os.getenv("GOOGLE_STUDIO_API"))
MAX_NUM_CONNECTIONS = int(os.getenv("MAX_NUM_CONNECTIONS"))

HOST_DB_USERNAME = str(os.getenv("HOST_DB_USERNAME"))
HOST_DB_PASSWORD = str(os.getenv("HOST_DB_PASSWORD"))
HOST_DB_URL = str(os.getenv("HOST_DB_URL"))
HOST_DB_PORT = str(os.getenv("HOST_DB_PORT"))
HOST_DB_DBNAME = str(os.getenv("HOST_DB_DBNAME"))
