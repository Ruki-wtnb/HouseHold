from ..categories import FixedName
from ..models import FixedCost as mo_Fixed

def set_fixed_id(new_fix: mo_Fixed, fixed_name: FixedName):

    if fixed_name == FixedName.Rent:
        fixed_id = 1
    elif fixed_name == FixedName.Water:
        fixed_id = 2
    elif fixed_name == FixedName.Electric:
        fixed_id = 3
    elif fixed_name == FixedName.Gas:
        fixed_id = 4
    elif fixed_name == FixedName.WiFi:
        fixed_id = 5
    
    new_fix.fixed_category_id = fixed_id
    
    return new_fix
