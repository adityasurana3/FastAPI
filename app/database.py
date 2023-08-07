from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# postgresql://<username>:<password>/@<ip-address>/<hostname>/<database_name>
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:admin@localhost/fastapi'
# client_encoding = utf8

engine = create_engine(SQLALCHEMY_DATABASE_URL, client_encoding='utf8')

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()