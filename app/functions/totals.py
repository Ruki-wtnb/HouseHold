
from ..models import Month

def return_num_month(month: Month):

    month_dict = {
    "Jan": "1",
    "Feb": "2",
    "Mar": "3",
    "Apr": "4",
    "May": "5",
    "Jun": "6",
    "Jul": "7",
    "Aug": "8",
    "Sep": "9",
    "Oct": "10",
    "Nov": "11",
    "Dec": "12"
    }

    return month_dict[month.name]


#async def calculate_total_income(year: str, month: str, db):
