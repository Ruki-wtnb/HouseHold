
from fastapi import APIRouter
from fastapi import Depends

from typing import List

from sqlalchemy import select

from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from app.functions.fixed import get_fixed_id

from ..categories import FixedName

from ..database import get_db

from ..functions import common as com
from ..functions import fixed

from ..models import FixedCosts as mo_Fixed

from ..schemas import FixedCosts as sc_Fixed


router = APIRouter(
    prefix='/fixed',
    tags=['fixed']
)


@router.post('')
async def create_fixed(account:sc_Fixed, fixed_name: FixedName, db:AsyncSession=Depends(get_db)):

    fixed_id = fixed.get_fixed_id(fixed_name)
    new_fix = mo_Fixed(**account.dict())
    new_fix.fixed_id = fixed_id

    return await com.execute_commit(new_fix, db)


@router.get('')
async def get_fixed(year_month: str, db:AsyncSession=Depends(get_db)):

    result: Result = await db.execute(
        select(mo_Fixed).filter(
            mo_Fixed.year_month == year_month
        )
    )

    return result.all()

@router.put('')
async def put_fixed(year_month:str, fixed_id: str, price: int, db:AsyncSession=Depends(get_db)):

    update_fixed_costs = await db.execute(
        select(
            mo_Fixed
            ).filter(
                mo_Fixed.year_month == year_month,
                mo_Fixed.fixed_id == fixed_id
            )
        )
    update_fixed_costs.price = price

    return com.execute_commit(update_fixed_costs, db)


@router.post('/bulk')
async def create_fixed(accounts:List[sc_Fixed], db:AsyncSession=Depends(get_db)):

    count = 0

    for account in accounts:
        new_fix = mo_Fixed(**account.dict())
        await com.execute_commit(new_fix, db)
        count += 1
    
    return {'Message': f'{count} spendings data registerd'}
