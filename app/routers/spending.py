from datetime import date

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from sqlalchemy import extract
from sqlalchemy import func
from sqlalchemy import join
from sqlalchemy import select

from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from typing import List

from ..database import get_db

from ..functions import spending as fs
from ..functions import common as com

from ..models import PaymentName
from ..models import SpendingName
from ..models import Spendings as md_Spendings
from ..models import SpendingCategories as md_SpendingCategories

from ..schemas import Spending as sc_Spending

router = APIRouter(
    prefix='/spending',
    tags=['spending']
)

@router.post('/', status_code=status.HTTP_200_OK)
async def create_spending(account:sc_Spending, spending_name: SpendingName, payment_name: PaymentName, db:AsyncSession=Depends(get_db)):

    new_spending = md_Spendings(**account.dict())
    new_spending = fs.set_spending_id(new_spending, spending_name)
    new_spending = fs.set_payment_id(new_spending, payment_name)

    # result: Result = await db.execute(
    #     select(md_Totals).filter(
    #         func.date_format(md_Totals.date, "%Y-%m") == account.date.strftime("%Y-%m")))

    return await fs.execute_commit(new_spending, db)


@router.get('/', status_code=status.HTTP_200_OK)
async def get_spending(db:AsyncSession=Depends(get_db)):
    result: Result = await db.execute(
        join(
            md_Spendings, md_SpendingCategories, 
            md_Spendings.spending_id == md_SpendingCategories.id
            ).select())
    return result.all()


@router.get('/{date}', status_code=status.HTTP_200_OK)
async def get_spending_by_date(date: date, db:AsyncSession=Depends(get_db)):
    result: Result = await db.execute(
        join(
            md_Spendings, md_SpendingCategories,
            md_Spendings.spending_id == md_SpendingCategories.id
            ).select().filter(md_Spendings.date == date))
    return result.all()


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
async def edit_spending(id:int, sc_spending:sc_Spending, db:AsyncSession=Depends(get_db)):
    
    update_spending = await fs.get_spending_by_id(id, db)

    update_spending.id = id
    update_spending.date = sc_spending.date
    update_spending.name = sc_spending.name
    update_spending.price = sc_spending.price
    update_spending.spending_id = sc_spending.spending_id
    update_spending.payment_id = sc_spending.payment_id
    
    return com.execute_commit(update_spending, db)


@router.delete('/{id}', status_code=status.HTTP_200_OK)
async def delete_spending(id: int, db:AsyncSession=Depends(get_db)):
    
    delete_spending = fs.get_spending_by_id(id, db)

    await db.delete(delete_spending)
    await db.commit()

    return {'Message': 'Delete succeed'}


@router.post('/bulk', status_code=status.HTTP_200_OK)
async def create_spending_bulk(accounts:List[sc_Spending], db:AsyncSession=Depends(get_db)):

    count = 0
    for account in accounts:
        new_account = md_Spendings(**account.dict())
        await fs.execute_commit(new_account, db)
        count += 1

    return {'Message': f'{count} spendings data registerd'}
