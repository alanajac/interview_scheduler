from fastapi import FastAPI, Depends
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from sqlalchemy import Column, String,Integer
from database import Base
from enum import Enum
from uuid import UUID, uuid4

app = FastAPI()

#SQLALCHEMY_DATABASE_URL = 'sqlite+pysqlite:///./db.sqlite3:'
#Connecting the database
SQLALCHEMY_DATABASE_URL = 'sqlite:///sqlite/sample.db'
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class DBUser(Base):
    __tablename__ = 'Users'
    id = Column(Integer,primary_key=True,index=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    middle_name = Column(String(50))
    email = Column(String(50))
    roles = Column(String)

Base.metadata.create_all(bind=engine)

class Roles(str,Enum):
    candidate = "candidate"
    interviewer = "interviewer"

#class Schedules()    

class User(BaseModel):
    #id: Optional[UUID]=uuid4()
    id: int
    first_name: str
    last_name: str
    middle_name: Optional[str]
    email: str
    roles: Roles
#    schedule: List[Schedules]

class Config:
        orm_mode = True
#@app.route('/user/', methods=['GET', 'POST']) 

#Methods to retrieve, post and add new information in the database

#@app.get("/user/")
#async def fetch_users():
#    return db.quer

#Retrieve one user
def get_user(db: Session, user_id: int):
    return db.query(DBUser).where(DBUser.id == user_id).first()
#Retrieves all users

def get_users(db: Session):
    return db.query(DBUser).all()
#Create a new user
def create_user(db: Session, user: User):
    db_user = DBUser(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

#routes to use our methods:
#create user
@app.post('/users/', response_model=User)
def create_user_view(user: User, db: Session = Depends(get_db)):
    db_user = create_user(db, user)
    return db_user
#retrieve all users
@app.get('/users/', response_model=List[User])
def get_user_view(db: Session = Depends(get_db)):
    return get_users(db)
#retrieve one user
@app.get('/user/{user_id}')
def get_user_view(user_id: int, db: Session = Depends(get_db)):
    return get_user(db, user_id)    

user1 = User(
        #id=uuid4(),
        id=10,
        first_name = "Alan",
        last_name = "Carmo",
        middle_name = "Alves",
        email = "alan.ajac@gmail.com",
        roles=Roles.interviewer)

#class Place(BaseModel):
#    name: str
#    description: Optional[str] = None
#    coffee: bool
#    wifi: bool
#    food: bool
#    lat: float
#    lng: float



#@app.post('/user/')
#async def create_User_view(user: User):
#    return user

#@app.get('/user/{user_id}')
#async def get_User_view(user: User):
#    return user


#class DBSchedule(Base):
#    __tablename__ = 'Schedules'
    
@app.get('/')
async def root(alan: int = 0):
    return {'message': 'Killing me softly!','alan': alan }