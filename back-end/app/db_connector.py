from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from fastapi import Depends
from config import DATABASE_PASS, DATABASE_NAME, PORT

URL_DATABASE = f'postgresql+asyncpg://postgres:{DATABASE_PASS}@localhost:{PORT}/{DATABASE_NAME}'


async_engine = create_async_engine(URL_DATABASE, echo=True)


AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,  
    autoflush=False,
    autocommit=False,
    expire_on_commit=False
)

Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()
