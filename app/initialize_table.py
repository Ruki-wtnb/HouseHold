
from app.models import IncomeCategories
from app.schemas import IncomeCategories as s_IC

import asyncio
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

def income_categories():

    DB_URL = "mysql+aiomysql://root@db_hh:3306/householddb?charset=utf8"
    engine = create_engine(DB_URL, echo=True)

    SessionClass = sessionmaker(engine)
    session = SessionClass()
    
    ic1 = s_IC(name="食費")
    ic2 = s_IC(name="外食費")
    ic3 = s_IC(name="生活用品")
    ic4 = s_IC(name="生活家具")
    ic5 = s_IC(name="生活家電")
        
    ic_list = [ic1, ic2, ic3, ic4, ic5]
        
    for ic in ic_list:
        data = IncomeCategories(**ic.dict())
        session.add(data).options()
        session.commit()

# python -c "import app.initialize_table; app.initialize_table.income_categories()"

if __name__ == "__main__":
    income_categories()
