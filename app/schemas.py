
from datetime import date
from pydantic import BaseModel


class Categories(BaseModel):
    name: str
    en_name: str

class FixedCost(BaseModel):
    year_month: str
    price: int
    fixed_category_id: int

class VariableCost(BaseModel):
    date: date
    name: str
    price: int

class VariableCostsValk(VariableCost):
    variable_category_id: int

class Totals(BaseModel):
    date: date
    price: int
