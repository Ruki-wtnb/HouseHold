
from fastapi import APIRouter
from fastapi import Depends

from typing import List

from sqlalchemy import select

from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db

from ..functions import common as com

from ..models import FixedCosts as md_FixedCosts
from ..models import FixedName

from ..schemas import FixedCosts as sc_FixedCosts


router = APIRouter(
    prefix='/fixed',
    tags=['fixed']
)

@router.post('')
async def create_fixed(account:sc_FixedCosts, fixed_name: FixedName, db:AsyncSession=Depends(get_db)):

    if fixed_name == FixedName.Rent:
        fixed_id = 1
    elif fixed_name == FixedName.Water:
        fixed_id = 2
    elif fixed_name == FixedName.Electric:
        fixed_id = 3
    elif fixed_name == FixedName.Gas:
        fixed_id = 4
    elif fixed_name == FixedName.WiFi:
        fixed_id = 5

    new_fix = md_FixedCosts(**account.dict())
    new_fix.fixed_id = fixed_id

    return await com.execute_commit(new_fix, db)


@router.get('')
async def get_fixed(year_month: str, db:AsyncSession=Depends(get_db)):

    result: Result = await db.execute(
        select(md_FixedCosts).filter(
            md_FixedCosts.year_month == year_month
        )
    )

    return result.all()

@router.put('')
async def put_fixed(year_month:str, fixed_id: str, price: int, db:AsyncSession=Depends(get_db)):

    update_fixed_costs = await db.execute(
        select(
            md_FixedCosts
            ).filter(
            md_FixedCosts.year_month == year_month
            ).filter(
            md_FixedCosts.fixed_id == fixed_id
            )
        )
    update_fixed_costs.price = price

    return com.execute_commit(update_fixed_costs, db)


@router.post('/bulk')
async def create_fixed(accounts:List[sc_FixedCosts], db:AsyncSession=Depends(get_db)):

    count = 0

    for account in accounts:
        new_fix = md_FixedCosts(**account.dict())
        await com.execute_commit(new_fix, db)
        count += 1
    
    return {'Message': f'{count} spendings data registerd'}
