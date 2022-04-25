

from fastapi import APIRouter
from fastapi import Depends
from fastapi import status

from sqlalchemy import and_
from sqlalchemy import extract
from sqlalchemy import func
from sqlalchemy import join
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy.engine.row import Row

from ..database import get_db

from ..models import FixedCosts as md_FixedCosts
from ..models import Incomes as md_Incomes
from ..models import Spendings as md_Spendings
from ..models import SpendingCategories as md_SpendingCategories
from ..models import Totals

from ..functions import totals

router = APIRouter(
    prefix='/totals',
    tags=['totals']
)

@router.get('/{year_month}')
async def get_spending(year_month: str, db:AsyncSession=Depends(get_db)):

    year_month_list = year_month.split('-')
    year = year_month_list[0]
    month = year_month_list[1]

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

    fixed_total_result: Result = await db.execute(
        select(
            func.sum(md_FixedCosts.price)
            ).filter(
                md_FixedCosts.year_month == year_month
            )
    )

    total_income = total_income_result.first()[0]
    total_spending = total_spending_result.first()[0]
    total_fixed = fixed_total_result.first()[0]
    total_costs = total_spending + total_fixed

    balance = total_income - total_costs
    res = {
        "収入": total_income,
        "支出": total_costs,
        "収支": balance
    }

    return res


@router.get('/spendings/{year_month}', status_code=status.HTTP_200_OK)
async def get_spendings_total(year_month: str, db:AsyncSession=Depends(get_db)):

    year_month = year_month.split('-')

    columns = [md_SpendingCategories.name, func.sum(md_Spendings.price)]

    result: Result = await db.execute(
        join(
            md_Spendings, md_SpendingCategories,
            md_Spendings.spending_id == md_SpendingCategories.id
        ).select(
        ).filter(
            extract('year', md_Spendings.date) == year_month[0]
        ).filter(
            extract('month', md_Spendings.date) == year_month[1]
        ).group_by(
            md_Spendings.spending_id).with_only_columns(columns)
        )

    return result.all()


@router.get('/incomes/{year_month}', status_code=status.HTTP_200_OK)
async def get_incomes_total(year_month: str, db:AsyncSession=Depends(get_db)):

    year_month = year_month.split('-')

    result: Result = await db.execute(
        select(
            func.sum(md_Incomes.price)
            ).filter(
                extract('year', md_Incomes.date) == year_month[0]
            ).filter(
                extract('month', md_Incomes.date) == year_month[1]
            )
    )
    return result.all()
