
from typing import List

from sqlalchemy import extract
from sqlalchemy import func
from sqlalchemy import join
from sqlalchemy import select
from sqlalchemy.engine import Result

from sqlalchemy.orm import Session

from ..models import FixedCost
from ..models import FixedCostCategory
from ..models import VariableCost
from ..models import VariableCostCategory

# TODO Async系のSQL文をquery系に全体的に変更する。
def get_fixed_result(year_month, db: Session):
    
    fixed_result = db.query(
        FixedCost.price,
        FixedCostCategory.en_name
        ).join(
            FixedCostCategory, 
            FixedCost.fixed_category_id == FixedCostCategory.id
        ).filter(
            FixedCost.year_month == year_month
        )
    return fixed_result

def get_variable_result(year_month_list, db: Session):

    variable_result =  db.query(
        VariableCost.price,
        VariableCostCategory.en_name
        ).join(
            VariableCostCategory, 
            VariableCost.variable_category_id == VariableCostCategory.id
        ).filter(
            extract('year', VariableCost.date) == year_month_list[0],
            extract('month', VariableCost.date) == year_month_list[1],
        )
    return variable_result

def get_total_result(spending_list):

    result = {}

    for spending in spending_list:
        result[spending[1]] = spending[0]

    spending_total = 0
    for r in result.keys():
        if r != 'income':
            spending_total += result[r]
        
    result['spending'] = spending_total
    result['balance'] = result['income'] - result['spending']
    
    return result

def add_missing_value(result):
    
    result_keys = result.keys()
    default_keys = ['rent', 'water', 'bolt', 'gas', 'wifi', 'restaurant', 'sanitizer', 'appliance', 'food', 'income', 'spending', 'balance', 'furniture']

    missing_keys = list(set(result_keys)^set(default_keys))

    for key in missing_keys:
        result[key] = 0

    return result

