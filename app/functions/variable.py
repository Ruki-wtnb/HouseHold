
from fastapi import HTTPException
from fastapi import status

from sqlalchemy import select

from sqlalchemy.engine import Result

from ..models import VariableCost as md_Variable

from ..schemas import VariableCost as sc_Variable

from ..categories import VariableName

async def get_variable_by_id(id, db):
    result: Result = db.query(md_Variable).filter(md_Variable.id == id)
    
    variable: md_Variable = result.first()[0]
    if not variable:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='variable not found')
    
    return variable


def set_variable_id(new_variable: md_Variable, variable_name: VariableName):
    
    if variable_name == VariableName.Food:
        new_variable.variable_category_id = 1
    elif variable_name == VariableName.EatingOut:
        new_variable.variable_category_id = 2
    elif variable_name == VariableName.Livingware:
        new_variable.variable_category_id = 3
    elif variable_name == VariableName.HomeAppliances:
        new_variable.variable_category_id = 4
    elif variable_name == VariableName.LivingFurniture:
        new_variable.variable_category_id = 5
    elif variable_name == VariableName.Income:
        new_variable.variable_category_id = 6
        
    if new_variable.variable_category_id == 6:
        new_variable.spending_flag = False
    else:
        new_variable.spending_flag = True
    
    return new_variable

def update_variable(existing_variable: md_Variable, update_variable: md_Variable):
    print(existing_variable.date)
    print(update_variable.__dir__())
    existing_variable.date = update_variable.date
    existing_variable.name = update_variable.name
    existing_variable.price = update_variable.price

    return existing_variable
