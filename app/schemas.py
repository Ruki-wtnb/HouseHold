
from datetime import date
from pydantic import BaseModel


class Categories(BaseModel):
    name: str
    en_name: str

class FixedCosts(BaseModel):
    year_month: str
    price: int
    fixed_category_id: int

class VariableCosts(BaseModel):
    date: date
    name: str
    price: int

class VariableCostsValk(VariableCosts):
    variable_category_id: int

class Totals(BaseModel):
    date: date
    price: int
