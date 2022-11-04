from fastapi import FastAPI, Depends,  HTTPException
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from sqlalchemy import Column, String,Integer
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

#retrieve one user -call
@app.get('/user/{user_id}')
def get_user_view(user_id: int, db: Session = Depends(get_db)):
    return get_user(db, user_id)

#Retrieves all users
def get_users(db: Session):
    return db.query(DBUser).all()

#Retrieve all users -call
@app.get('/users/', response_model=List[User])
def get_user_view(db: Session = Depends(get_db)):
    return get_users(db)

#Create a new user
def create_user(db: Session, user: User):
    db_user = DBUser(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user
#Create a new user-call
@app.post('/users/', response_model=User)
def create_user_view(user: User, db: Session = Depends(get_db)):
    db_user = create_user(db, user)
    return db_user


#attempt 5
#delete a user
def delete_user(db: Session, user_id: int):
    user =  get_user(db,user_id)
    if user:
        db.delete(user)
        db.commit()
        return



#delete a user-call
@app.delete('/user/{user_id}')
async def delete_user_view(user_id: int,db: Session = Depends(get_db)):
    return delete_user(db,user_id)
#delete user attempt 1
'''
    #    return db.query(DBUser).delete(user).where(DBUser.id == user_id)
    #for user in db:
    #    db.remove(user).where(user.id == user_id).first()
    #    db.commit()
    #    return  {"ok": True}

'''
#delete user # --attempt 2
'''
def delete_user(db: Session, user_id: int):
    with Session(engine) as session:
        idx = session.get(User, user_id)
        if not idx:
            raise HTTPException(status_code=404, detail="index not found")
        session.delete(idx).first()
        session.commit()
        return {"ok": True}
'''    

#delete user # attempt 3
    
'''
def delete_user(db: Session, user_id: int): 
    for user in db:
        if user_id== user.id:
            db.remove(user)
            db.commit()
            db.refresh(db)
            return
        #db.remove(user).where(user.id == user_id)
    #    db.query(DBUser).delete(user).where(user.id == user_id)
'''
            
#delete user attempt 4
'''
def delete_user(db: Session, user_id: int):
    db.delete(DBUser).where(DBUser.id == user_id)
    db.commit()
    return
'''
#routes to use our methods:
#create user




          
@app.put("/user/{user_id}")
async def update_user_view(user_id: int,user: User, db: Session = Depends(get_db)):
   user_model = db.query(DBUser).filter(DBUser.id == user_id).first() 
   if user_model is None:
    raise HTTPException(
        status_code=404,detail=f"ID{user_id}: Does not exist"
    )
   user_model.id =  user.id
   user_model.first_name = user.first_name
   user_model.last_name = user.last_name
   user_model.middle_name = user.middle_name
   user_model.email = user.email
   user_model.roles = user.roles

   db.add(user_model)
   db.commit()
   return user  

user1 = User(
        #id=uuid4(),
        id=10,
        first_name = "Alan",
        last_name = "Carmo",
        middle_name = "Alves",
        email = "alan.ajac@gmail.com",
        roles=Roles.interviewer)

#class DBSchedule(Base):
#    __tablename__ = 'Schedules'
    
@app.get('/')
async def root(alan: int = 0):
    return {'message': 'Killing me softly!','alan': alan }