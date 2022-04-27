
from fastapi import APIRouter
from fastapi import Depends
from fastapi import status

from sqlalchemy import and_, text
from sqlalchemy import column
from sqlalchemy import extract
from sqlalchemy import func
from sqlalchemy import join
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy.engine.row import Row

from ..database import get_db

from ..models import FixedCosts as md_FixedCosts
from ..models import FixedCategories as md_FixedCategories
from ..models import Incomes as md_Incomes
from ..models import Spendings as md_Spendings
from ..models import SpendingCategories as md_SpendingCategories


router = APIRouter(
    prefix='/totals',
    tags=['totals']
)

@router.get('/{year_month}')
async def get_spending(year_month: str, db:AsyncSession=Depends(get_db)):
    
    # 年月
    year_month_list = year_month.split('-')
    year = year_month_list[0]
    month = year_month_list[1]
    
    total_income = 0
    total_spending = 0
    total_fixed = 0

    total_income_result: Result = await db.execute(
        select(
            func.sum(md_Incomes.price)
            ).filter(
                extract('year', md_Incomes.date) == year
            ).filter(
                extract('month', md_Incomes.date) == month
            )
    )
    
    total_spending_result: Result = await db.execute(
        select(
            func.sum(md_Spendings.price)
            ).filter(
                extract('year', md_Spendings.date) == year
            ).filter(
                extract('month', md_Spendings.date) == month
            )
        )

    total_fixed_result: Result = await db.execute(
        select(
            func.sum(md_FixedCosts.price)
            ).filter(
                md_FixedCosts.year_month == year_month
            )
    )

    
    total_spending = total_spending_result.first()[0] if total_spending_result != None else 0
    total_fixed = total_fixed_result.first()[0] if total_fixed_result != None else 0
    total_costs = total_spending + total_fixed

    total_income = total_income_result.first()[0] if total_income_result != None else 0

    balance = total_income - total_costs
    res = {
        "収入": total_income,
        "支出": total_costs,
        "収支": balance
    }

    return res

@router.get('/list/{year_month}', status_code=status.HTTP_200_OK)
async def get_totals(year_month: str, db:AsyncSession=Depends(get_db)):
    
    year_month_list = year_month.split('-')

    income_result: Result = await db.execute(
        select(
            md_Incomes.name, func.sum(md_Incomes.price)
            ).filter(
                extract('year', md_Incomes.date) == year_month_list[0]
            ).filter(
                extract('month', md_Incomes.date) == year_month_list[1]
            )
    )

    spending_columns = [md_SpendingCategories.name, func.sum(md_Spendings.price)]
    spending_result: Result = await db.execute(
        join(
            md_Spendings, md_SpendingCategories,
            md_Spendings.spending_id == md_SpendingCategories.id
        ).select(
        ).filter(
            extract('year', md_Spendings.date) == year_month_list[0]
        ).filter(
            extract('month', md_Spendings.date) == year_month_list[1]
        ).group_by(
            md_Spendings.spending_id
            ).with_only_columns(spending_columns)
        )
    
    fixed_columns = [md_FixedCategories.name, func.sum(md_FixedCosts.price)]
    fixed_result: Result = await db.execute(
        join(
            md_FixedCosts, md_FixedCategories,
            md_FixedCosts.fixed_id == md_FixedCategories.id
        ).select(
        ).filter(
            md_FixedCosts.year_month == year_month
        ).group_by(
            md_FixedCosts.fixed_id
            ).with_only_columns(fixed_columns)
        )
    

    # income_result = list(income_result.all()[0])
    # income_result.insert(0, '収入')
    # tuple(income_result)
    
    list_result = [income_result, spending_result, fixed_result]
    total_result = []
    
    for rl in list_result:
        for r in rl.all():
            total_result.append(r)

    return total_result
