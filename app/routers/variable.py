from datetime import date

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from sqlalchemy import extract
from sqlalchemy import func
from sqlalchemy import join
from sqlalchemy import select

from sqlalchemy.orm import Session

from sqlalchemy.engine import Result

from typing import List

from ..categories import VariableName

from ..database import get_db

from ..functions import variable as va
from ..functions import common as com

from ..models import VariableCost as md_Variable
from ..models import VariableCostCategory as md_VariableCategories

from ..schemas import VariableCost as sc_Variable
from ..schemas import VariableCostsValk as VariableCostsValk

router = APIRouter(
    prefix='/variable',
    tags=['variable']
)

@router.post('/', status_code=status.HTTP_201_CREATED)
def create_spending(account:sc_Variable, variable_name: VariableName, db:Session=Depends(get_db)):

    new_variable = md_Variable(**account.dict())
    new_variable = va.set_variable_id(new_variable, variable_name)

    db.add(new_variable)
    db.commit()
    db.refresh(new_variable)

    return new_variable


@router.get('/', status_code=status.HTTP_200_OK)
def get_spending(db:Session=Depends(get_db)):
    result = db.query(md_Variable)
    return result.all()


# @router.get('/{date}', status_code=status.HTTP_200_OK)
#  def get_spending_by_date(date: date, db:Session=Depends(get_db)):
#     result: Result = await db.execute(
#         join(
#             md_Variable, md_VariableCategories,
#             md_Variable.variable_category_id == md_VariableCategories.id
#         ).select().filter(md_Variable.date == date)
#     )
#     return result.all()


# @router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
#  def update_variable(id: int, variable_name: VariableName, account:sc_Variable, db:Session=Depends(get_db)):
    
#     existing_variable = await va.get_variable_by_id(id, db)

#     update_variable = md_Variable(**account.dict())
#     update_variable = va.set_variable_id(update_variable, variable_name)

#     new_existing_variable = va.update_variable(update_variable, existing_variable)

#     return await com.execute_commit(new_existing_variable)


# @router.delete('/{id}', status_code=status.HTTP_200_OK)
#  def delete_spending(id: int, db:Session=Depends(get_db)):
    
#     delete_spending = va.get_variable_by_id(id, db)

#     await db.delete(delete_spending)
#     await db.commit()

#     return {'Message': 'Delete succeed'}


@router.post('/bulk', status_code=status.HTTP_200_OK)
def create_spending_bulk(accounts:List[VariableCostsValk], db:Session=Depends(get_db)):
    
    count = 0
    for account in accounts:
        new_variable = md_Variable(**account.dict())
        db.add(new_variable)
        db.commit()
        db.refresh(new_variable)
        count += 1

    return {'Message': f'{count} spendings data registerd'}
