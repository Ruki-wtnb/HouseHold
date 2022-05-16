
from fastapi import APIRouter
from fastapi import Depends

from typing import List

from sqlalchemy import select

from sqlalchemy.orm import Session

from sqlalchemy.engine import Result


from app.functions.fixed import set_fixed_id

from ..categories import FixedName

from ..database import get_db

from ..functions import common as com
from ..functions import fixed

from ..models import FixedCost as mo_Fixed

from ..schemas import FixedCost as sc_Fixed


router = APIRouter(
    prefix='/fixed',
    tags=['fixed']
)


@router.post('')
async def create_fixed(account:sc_Fixed, fixed_name: FixedName, db:Session=Depends(get_db)):

    new_fix = mo_Fixed(**account.dict())
    new_fix = fixed.set_fixed_id(new_fix, fixed_name)

    return com.execute_commit(new_fix, db)


@router.get('')
async def get_fixed(year_month: str, db:Session=Depends(get_db)):

    result = db.query(
        mo_Fixed
        ).filter(
            mo_Fixed.year_month == year_month
            ).all()

    return result

# @router.put('')
# async def put_fixed(year_month:str, fixed_id: str, price: int, db:Session=Depends(get_db)):

#     update_fixed_costs = await db.execute(
#         select(
#             mo_Fixed
#             ).filter(
#                 mo_Fixed.year_month == year_month,
#                 mo_Fixed.fixed_id == fixed_id
#             )
#         )
#     update_fixed_costs.price = price

#     return com.execute_commit(update_fixed_costs, db)


@router.post('/bulk')
async def create_fixed(accounts:List[sc_Fixed], db:Session=Depends(get_db)):

    count = 0

    for account in accounts:
        new_fix = mo_Fixed(**account.dict())
        db.add(new_fix)
        db.commit()
        db.refresh(new_fix)
        # com.execute_commit(new_fix, db)
        count += 1
    
    return {'Message': f'{count} spendings data registerd'}
