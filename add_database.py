import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker



#SQLALCHEMY_DATABASE_URL = 'sqlite+pysqlite:///./db.sqlite3:'
#Connecting the database
SQLALCHEMY_DATABASE_URL = 'sqlite:///sqlite/sample_fill.db'

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True, future=True,connect_args={'check_same_thread': False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

