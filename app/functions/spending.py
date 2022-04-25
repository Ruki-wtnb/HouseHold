
from fastapi import HTTPException
from fastapi import status

from sqlalchemy import select

from sqlalchemy.engine import Result

from ..models import Spendings as md_Spendings
from ..models import SpendingName
from ..models import PaymentName

async def get_spending_by_id(id, db):
    result: Result = await db.execute(
        select(md_Spendings).filter(md_Spendings.id == id))
    
    spending: md_Spendings = result.first()[0]
    if not spending:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='spending not found')
    
    return spending


async def execute_commit(spending, db):

    db.add(spending)
    await db.commit()
    await db.refresh(spending)
    return spending


def set_spending_id(new_spending: md_Spendings, spending_name: SpendingName):
    
    if spending_name == SpendingName.Food:
        new_spending.spending_id = 1
    elif spending_name == SpendingName.EatingOut:
        new_spending.spending_id = 2
    elif spending_name == SpendingName.Livingware:
        new_spending.spending_id = 3
    elif spending_name == SpendingName.HomeAppliances:
        new_spending.spending_id = 4
    elif spending_name == SpendingName.LivingFurniture:
        new_spending.spending_id = 5
    
    return new_spending

def set_payment_id(new_spending: md_Spendings, payment_name: PaymentName):

    if payment_name == PaymentName.QR:
        new_spending.payment_id = 1
    elif payment_name == PaymentName.Card:
        new_spending.payment_id = 2
    elif payment_name == PaymentName.Cash:
        new_spending.payment_id = 3
    
    return new_spending
