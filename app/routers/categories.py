
from fastapi import APIRouter
from fastapi import Depends

from typing import List

from sqlalchemy.orm import Session
from sqlalchemy.engine import Result

from ..schemas import Categories
from ..models import FixedCostCategory
from ..models import VariableCostCategory
from ..categories import CategoryName
from ..database import get_db

router = APIRouter(
    prefix='/categories',
    tags=['categories']
)

@router.get('/categories')
def get_categories(category_name: CategoryName, db:Session=Depends(get_db)):

    if category_name == CategoryName.FixedCostsCategories:
        result: Result = db.query(FixedCostCategory).all()
    elif category_name == CategoryName.VariableCostsCategories:
        result: Result = db.query(VariableCostCategory).all()

    return result


@router.post('/categories')
def create_categories(categories: List[Categories], category_name: CategoryName, db: Session=Depends(get_db)):

    count = 0

    for cate in categories: 
        if category_name == CategoryName.FixedCostsCategories:
            new_cate = FixedCostCategory(**cate.dict())
        elif category_name == CategoryName.VariableCostsCategories:
            new_cate = VariableCostCategory(**cate.dict())
        
        db.add(new_cate)
        db.commit()
        db.refresh(new_cate)
        count += 1
    
    return  {'Message': f'{count} categories data registerd'}
