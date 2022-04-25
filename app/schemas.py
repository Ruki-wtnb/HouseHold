
from datetime import date
from pydantic import BaseModel


class Account(BaseModel):
    date: date
    name: str
    price: int

class Spending(Account):
    spending_id: int
    payment_id: int

class Totals(BaseModel):
    date: date
    price: int

class Categories(BaseModel):
    name: str

class FixedCosts(BaseModel):
    year_month: str
    price: int
    fixed_id: int
