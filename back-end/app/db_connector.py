from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config import DATABASE_PASS, DATABASE_NAME, PORT, HOST_DB_DBNAME,HOST_DB_PASSWORD,HOST_DB_PORT,HOST_DB_URL,HOST_DB_USERNAME
from contextlib import asynccontextmanager
import ssl

HOST_DATBASE =""
# HOST_DATBASE = f"postgresql+asyncpg://{HOST_DB_USERNAME}:{HOST_DB_PASSWORD}@{HOST_DB_URL}:{HOST_DB_PORT}/{HOST_DB_DBNAME}"
URL_DATABASE = f'postgresql+asyncpg://postgres:{DATABASE_PASS}@localhost:{PORT}/{DATABASE_NAME}'

if HOST_DATBASE:
    URL_DATABASE = HOST_DATBASE


ssl_context = ssl.create_default_context(cafile="security_folder\ca.pem")
engine = create_async_engine(
    URL_DATABASE,
    connect_args={"ssl": ssl_context} if HOST_DATBASE else {}
)
AsyncSessionLocal = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)

Base = declarative_base()


async def get_db():
    """
    Async context manager to provide a database session.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
