from ..categories import FixedName

def get_fixed_id(fixed_name: FixedName):

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
    else:
        fixed_id = 1

    return fixed_id
