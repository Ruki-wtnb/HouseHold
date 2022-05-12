
from typing import List

from sqlalchemy import extract
from sqlalchemy import func
from sqlalchemy import join
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import FixedCosts as FixedCosts
from ..models import FixedCostsCategories
from ..models import VariableCosts 
from ..models import VariableCostsCategories

async def get_fixed_result(year_month, fixed_columns, db):
    
    fixed_result: Result = await db.execute( 
        join(
            FixedCosts, FixedCostsCategories,
            FixedCosts.fixed_category_id == FixedCostsCategories.id
        ).select(
        ).filter(
            FixedCosts.year_month == year_month
        ).group_by(
            FixedCosts.fixed_category_id
        ).with_only_columns(
            fixed_columns
        )
    )
    return fixed_result

async def get_variable_result(year_month_list, variable_columns, db):

    variable_result: Result = await db.execute(
        join(
            VariableCosts, VariableCostsCategories,
            VariableCosts.variable_category_id == VariableCostsCategories.id
        ).select(
        ).filter(
            extract('year', VariableCosts.date) == year_month_list[0],
            extract('month', VariableCosts.date) == year_month_list[1],
        ).group_by(
            VariableCosts.variable_category_id
        ).with_only_columns(
            variable_columns
        )
    )
    return variable_result

def get_total_result(spending_list):

    result = {}
    
    for spending in spending_list:
        for sp in spending:
            result[sp[0]] = sp[1]

    spending_total = 0
    for sl in spending_list:
        for s in sl:
            if s['en_name'] != 'income':
                spending_total += s['price']
    
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

