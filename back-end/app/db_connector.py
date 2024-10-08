from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config import DATABASE_PASS, DATABASE_NAME, PORT
from contextlib import asynccontextmanager

URL_DATABASE = f'postgresql+asyncpg://postgres:{DATABASE_PASS}@localhost:{PORT}/{DATABASE_NAME}'

engine = create_async_engine(URL_DATABASE)
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
