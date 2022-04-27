# uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# アドミンユーザ
# {
# }

'''
user名: 
password名
'''

from fastapi import FastAPI

from .routers import fixed
from .routers import categories
from .routers import incomes
from .routers import spending
from .routers import totals

app = FastAPI()

app.include_router(fixed.router)
app.include_router(categories.router)
app.include_router(incomes.router)
app.include_router(spending.router)
app.include_router(totals.router)
