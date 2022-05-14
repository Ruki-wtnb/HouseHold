#https://tkstock.site/2021/12/03/heroku-sqlalchmy-create_engine-%E3%82%A8%E3%83%A9%E3%83%BC-nosuchmoduleerror/

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

ASYNC_DB_URL = "mysql+aiomysql://root@db_hh:3306/householddb?charset=utf8"

async_engine  = create_async_engine(ASYNC_DB_URL, echo=True)
async_session = sessionmaker(autocommit=False, autoflush=False, bind=async_engine, class_=AsyncSession)

Base = declarative_base()

async def get_db():
    async with async_session() as session:
        yield session
