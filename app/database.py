from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
from .config import settings

# postgresql://<username>:<password>/@<ip-address>/<hostname>/<database_name>
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'
# client_encoding = utf8

engine = create_engine(SQLALCHEMY_DATABASE_URL, client_encoding='utf8')

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

############################ To connect the postges with python so that we can execute raw sql ############################
# while True:
#     try:
#         conn = psycopg2.connect(database='fastapi', user='postgres', password='admin', host='localhost',
#                                 cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connected")
#         break
#     except Exception as error:
#         print("Connection to data base failed")
#         print("Error: ", error)
