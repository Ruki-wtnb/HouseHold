from fastapi import APIRouter
from fastapi import Depends
from fastapi import status

from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db

from ..functions import totals as to


router = APIRouter(
    prefix='/totals',
    tags=['totals']
)

@router.get('/list/{year_month}', status_code=status.HTTP_200_OK)
def get_totals(year_month: str, db:AsyncSession=Depends(get_db)):

    year_month_list = year_month.split('-')

    fixed_result: Result = to.get_fixed_result(year_month, db)
    variable_result: Result = to.get_variable_result(year_month_list, db)

    fixed_list = fixed_result.all()
    variable_list = variable_result.all()
    spending_list = fixed_list + variable_list
    
    result_dict = to.add_missing_value(spending_list)
    result = to.get_total_result(result_dict)
    

    return result
