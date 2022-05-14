
import os

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

ASYNC_DB_URL = 'mysql+aiomysql://{user}:{password}@{host}/{db}?charset=utf8'.format(**{
    'user': os.getenv('DB_USER', os.environ['DB_USERNAME']),
    'password': os.getenv('DB_PASSWORD', os.environ['DB_PASSWORD']),
    'host': os.getenv('DB_HOST', os.environ['DB_HOSTNAME']),
    'db': os.getenv('DB_NAME', os.environ['DB_NAME']),
})
#"mysql+aiomysql://root@db_hh:3306/householddb?charset=utf8"

async_engine  = create_async_engine(ASYNC_DB_URL, echo=True)
async_session = sessionmaker(autocommit=False, autoflush=False, bind=async_engine, class_=AsyncSession)

Base = declarative_base()

async def get_db():
    async with async_session() as session:
        yield session
