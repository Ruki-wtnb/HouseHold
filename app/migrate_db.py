'''
DBマイグレーション用ファイル
'''
# 初期化 python -c "import app.migrate_db; app.migrate_db.reset_database()"
#　作成　　python -m app.migrate_db

from sqlalchemy import create_engine

from .models import Base

DB_URL = "postgresql://root@db_hh:3306/householddb?charset=utf8"
#"mysql+pymysql://root@db_hh:3306/householddb?charset=utf8"

engine = create_engine(DB_URL, echo=True)

def reset_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

def create_database():
    Base.metadata.create_all(bind=engine)

def drop_table():
    Base.metadata.drop_all(bind=engine)


if __name__ == "__main__":
    reset_database()
