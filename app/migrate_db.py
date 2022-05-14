'''
DBマイグレーション用ファイル
'''
# 初期化 python -c "import app.migrate_db; app.migrate_db.reset_database()"
#　作成　　python -m app.migrate_db

from sqlalchemy import create_engine

from .models import Base

DB_URL = "postgresql://togjxwubllzqzv:969d165b0f23231b52209e0372d73db8a36c50971f1366deaf2beffa33ab1c40@ec2-44-196-223-128.compute-1.amazonaws.com:5432/d2aslj2v9r3hhn"
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
