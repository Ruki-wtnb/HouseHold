from fastapi import APIRouter
from fastapi import Depends
from fastapi import Response
from fastapi import status

from sqlalchemy import extract
from sqlalchemy import func
from sqlalchemy import join
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db

from ..functions import totals as to

from ..models import FixedCosts as FixedCosts
from ..models import FixedCostsCategories
from ..models import VariableCosts 
from ..models import VariableCostsCategories


router = APIRouter(
    prefix='/totals',
    tags=['totals']
)

@router.get('/list/{year_month}', status_code=status.HTTP_200_OK)
async def get_totals(year_month: str, response: Response, db:AsyncSession=Depends(get_db)):
    response.headers["Access-Control-Allow-Origin"] = 'http://127.0.0.1:5500'

    year_month_list = year_month.split('-')

    fixed_columns = [FixedCostsCategories.en_name, func.sum(FixedCosts.price).label('price')]
    fixed_result: Result = await  to.get_fixed_result(year_month, fixed_columns, db)

    variable_columns = [VariableCostsCategories.en_name, func.sum(VariableCosts.price).label('price')]
    variable_result: Result = await to.get_variable_result(year_month_list, variable_columns, db)
    
    fixed_list = fixed_result.all()
    variable_list = variable_result.all()
    spending_list = [fixed_list, variable_list]

    result = to.get_total_result(spending_list)
    result = to.add_missing_value(result)

    return result
