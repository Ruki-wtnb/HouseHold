
from sqlalchemy import extract
from sqlalchemy import func

from sqlalchemy.orm import Session

from ..models import FixedCost
from ..models import FixedCostCategory
from ..models import VariableCost
from ..models import VariableCostCategory


def get_fixed_result(year_month, db: Session):
    
    fixed_result = db.query(
        FixedCostCategory.en_name,
        FixedCost.price
        ).join(
            FixedCostCategory, 
            FixedCost.fixed_category_id == FixedCostCategory.id
            ).filter(
                FixedCost.year_month == year_month
                )

    return fixed_result


def get_variable_result(year_month_list, db: Session):

    variable_result =  db.query(
        VariableCostCategory.en_name,
         func.sum(VariableCost.price)
        ).join(
            VariableCostCategory, 
            VariableCost.variable_category_id == VariableCostCategory.id
            ).filter(
                extract('year', VariableCost.date) == year_month_list[0],
                extract('month', VariableCost.date) == year_month_list[1],
            ).group_by(
                VariableCost.variable_category_id
            )

    return variable_result


def get_total_result(result_dict):

    spending_total = 0
    
    for key in result_dict.keys():
        if key != 'income':
            spending_total += result_dict[key]
        
    result_dict['spending'] = spending_total
    result_dict['balance'] = result_dict['income'] - result_dict['spending']
    
    return result_dict


def add_missing_value(result):
    
    result_dict = {}

    for re in result:
        result_dict[re[0]] = re[1]
    
    result_keys = result_dict.keys()

    default_keys = ['rent', 'water', 'gas', 'bolt', 'wifi', 'food','restaurant', 'sanitizer', 'appliance', 'furniture', 'income', 'spending', 'balance']

    missing_keys = list(set(result_keys)^set(default_keys))

    for key in missing_keys:
        result_dict[key] = 0

    return result_dict
