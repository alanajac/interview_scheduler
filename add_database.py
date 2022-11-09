import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker



#SQLALCHEMY_DATABASE_URL = 'sqlite+pysqlite:///./db.sqlite3:'
#Connecting the database
SQLALCHEMY_DATABASE_URL = 'sqlite:///sqlite/sample.db'
#SQLALCHEMY_DATABASE_URI = (os.environ.get('SQLALCHEMY_DATABASE_URL') or \
#    'sqlite:///'+os.path.join("/sqlite", 'sample.db'))+'?check_same_thread=False'
#SQLALCHEMY_TRACK_MODIFICATIONS = False
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True, future=True,connect_args={'check_same_thread': False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


    
#@app.route('/user/', methods=['GET', 'POST']) 

#Methods to retrieve, post and add new information in the database

#@app.get("/user/")
#async def fetch_users():
#    return db.quer