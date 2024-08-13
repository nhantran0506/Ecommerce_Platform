from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

URL_DATABASE = 'postgresql://postgres:1234!@localhost:1234/ecommerce_platform'

engine = create_engine(URL_DATABASE)

SessionLocal = sessionmaker(auto_commit=False, auto_flush=False, bind = engine)

Base = declarative_base()