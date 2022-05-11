
from re import T
from fastapi import APIRouter
from fastapi import Depends
from fastapi import Response
from fastapi import status

from sqlalchemy import extract
from sqlalchemy import func
from sqlalchemy import join
from sqlalchemy import select
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
    spending_total = 0
    for sl in spending_list:
        for s in sl:
            if s["en_name"] != "income":
                spending_total += s["price"]
    
    # total_dict = dict(zip(income_list.keys(), income_list))

    result = [fixed_list, variable_list]

    return result












# @router.get('/{year_month}')
# async def get_spending(year_month: str, db:AsyncSession=Depends(get_db)):
    
#     # 年月
#     year_month_list = year_month.split('-')
#     year = year_month_list[0]
#     month = year_month_list[1]
    
#     total_total = 0
#     total_spending = 0
#     total_fixed = 0

#     total_total_result: Result = await db.execute(
#         select(
#             func.sum(md_totals.price)
#             ).filter(
#                 extract('year', md_totals.date) == year
#             ).filter(
#                 extract('month', md_totals.date) == month
#             )
#     )
    
#     total_spending_result: Result = await db.execute(
#         select(
#             func.sum(md_SpenVariableCosts
#             ).filter(
#                 extract('year', md_SpenVariableCosts== year
#             ).filter(
#                 extract('month', md_SpenVariableCosts== month
#             )
#         )

#     total_fixed_result: Result = await db.execute(
#         select(
#             func.sum(FixedCosts.price)
#             ).filter(
#                 FixeCosts.year_mh == year_mon#         lter(
#      CategoriVariableCostsCategories 
#     total_spending = total_spending_result.first()[0] if total_spending_result != None else 0
#     total_fixed = total_fixed_result.first()[0] if total_fixed_result != None else 0
#     total_costs = total_spending + total_fixed

#     total_total = total_total_result.first()[0] if total_total_result != None else 0

#     balance = total_total - total_costs
#     res = {
#         "収入": total_total,
#         "支出": total_costs,
#         "収支": balance
#     }

#     return res
