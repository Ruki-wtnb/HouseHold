
from sqlalchemy import select
from fastapi import APIRouter
from fastapi import Depends
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result

from ..schemas import Categories
from ..models import FixedCostsCategories
from ..models import VariableCostsCategories
from ..categories import CategoryName
from ..database import get_db



router = APIRouter(
    prefix='/categories',
    tags=['categories']
)


@router.get('/categories')
async def get_categories(category_name: CategoryName, db:AsyncSession=Depends(get_db)):

    if category_name == CategoryName.FixedCostsCategories:
        result: Result = await db.execute(select(FixedCostsCategories))
    elif category_name == CategoryName.VariableCostsCategories:
        result: Result = await db.execute(select(VariableCostsCategories))

    return result.all()


@router.post('/categories')
async def create_categories(categories: List[Categories], category_name: CategoryName, db: AsyncSession=Depends(get_db)):

    count = 0

    for cate in categories: 
        if category_name == CategoryName.FixedCostsCategories:
            new_cate = FixedCostsCategories(**cate.dict())
        elif category_name == CategoryName.VariableCostsCategories:
            new_cate = VariableCostsCategories(**cate.dict())
        
        db.add(new_cate)
        await db.commit()
        count += 1
    
    return  {'Message': f'{count} categories data registerd'}
