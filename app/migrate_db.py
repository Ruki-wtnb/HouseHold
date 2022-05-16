# '''
# DBマイグレーション用ファイル
# '''

# import os
# from sqlalchemy import create_engine
# from .models import Base

# DB_URL = 'mysql+aiomysql://{user}:{password}@{host}/{db}?charset=utf8'.format(**{
#     'user': os.getenv('DB_USER', os.environ['DB_USERNAME']),
#     'password': os.getenv('DB_PASSWORD', os.environ['DB_PASSWORD']),
#     'host': os.getenv('DB_HOST', os.environ['DB_HOSTNAME']),
#     'db': os.getenv('DB_NAME', os.environ['DB_NAME']),
# })
# SQLALCHEMY_TRACK_MODIFICATIONS = False
# SQLALCHEMY_ECHO = False
# #"mysql+pymysql://root@db_hh:3306/householddb?charset=utf8"

# engine = create_engine(DB_URL, echo=True)

# def reset_database():
#     Base.metadata.drop_all(bind=engine)
#     Base.metadata.create_all(bind=engine)

# def create_database():
#     Base.metadata.create_all(bind=engine, lazy='joined')

# def drop_table():
#     Base.metadata.drop_all(bind=engine)


# if __name__ == "__main__":
#     reset_database()
