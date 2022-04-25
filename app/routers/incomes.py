
from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db

from ..models import Incomes as md_Incomes

from ..schemas import Account as sc_Account


router = APIRouter(
    prefix='/income',
    tags=['income']
)


@router.post('')
async def create_income(account:sc_Account, db:AsyncSession=Depends(get_db)):

    new_income = md_Incomes(**account.dict())

    db.add(new_income)
    await db.commit()
    await db.refresh(new_income)

    return new_income


@router.get('')
async def get_income(db:AsyncSession=Depends(get_db)):

    result: Result = await db.execute(
        md_Incomes
    )

    return result.all()

@router.put('')
async def put_income(id: int, account:sc_Account, db:AsyncSession=Depends(get_db)):
    pass
