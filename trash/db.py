import os
import pymysql
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

host = os.getenv("DB_HOST")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_NAME")

DB_URL = f'mysql+pymysql://{user}:{password}@{host}:3306/{db_name}'

engine = create_engine(DB_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

