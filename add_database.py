from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from sqlalchemy import Column, String,Integer


#SQLALCHEMY_DATABASE_URL = 'sqlite+pysqlite:///./db.sqlite3:'
#Connecting the database
SQLALCHEMY_DATABASE_URL = 'sqlite:///sqlite/sample.db'
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

#@app.route('/user/', methods=['GET', 'POST']) 

#Methods to retrieve, post and add new information in the database

#@app.get("/user/")
#async def fetch_users():
#    return db.quer