# uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# アドミンユーザ
# {
# }

'''
user名: 
password名
'''

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .models import Base
from .database import engine

from .routers import categories
from .routers import fixed
from .routers import variable
from .routers import totals

app = FastAPI()

Base.metadata.create_all(engine)

origins = [
    'http://127.0.0.1:5500',
    'http://127.0.0.1:5501',
    'https://ruki-wtnb.github.io',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(categories.router)
app.include_router(fixed.router)
app.include_router(variable.router)
app.include_router(totals.router)
