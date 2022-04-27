
from sqlalchemy import select
from fastapi import APIRouter
from fastapi import Depends
from typing import List

from sqlalchemy import func, join
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result

from ..schemas import Account, Categories
from ..schemas import Totals as sc_totals
from ..schemas import FixedCosts as sc_fixed
from ..models import FixedCategories, PaymentCategories, SpendingCategories
from ..models import FixedCosts as md_fixed
from ..models import CateName, FixedName
from ..database import get_db



router = APIRouter(
    prefix='/categories',
    tags=['categories']
)


@router.get('/categories')
async def get_categories(cate_name: CateName, db:AsyncSession=Depends(get_db)):

    if cate_name == CateName.SpendingCategories:
        result: Result = await db.execute(select(SpendingCategories))
    elif cate_name == CateName.PaymentCategorie:
        result: Result = await db.execute(select(PaymentCategories))
    elif cate_name == CateName.FixedCategories:
        result: Result = await db.execute(select(FixedCategories))
        
    return result.all()


@router.post('/categories')
async def create_categories(categories: List[Categories], cate_name: CateName, db: AsyncSession=Depends(get_db)):

    count = 0

    for cate in categories: 
        if cate_name == CateName.SpendingCategories:
            new_cate = SpendingCategories(**cate.dict())
        elif cate_name == CateName.PaymentCategorie:
            new_cate = PaymentCategories(**cate.dict())
        elif cate_name == CateName.FixedCategories:
            new_cate = FixedCategories(**cate.dict())

        db.add(new_cate)
        await db.commit()
        count += 1
    
    return  {'Message': f'{count} categories data registerd'}
