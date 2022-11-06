#libraries
from fastapi import FastAPI,HTTPException,Depends
from pydantic import BaseModel,Field
from uuid import UUID, uuid4
from typing import Union,List,Optional
from enum import Enum
from datetime import datetime
from sqlalchemy.orm import Session
#other files
import models
from add_database import engine,SessionLocal
#from agenda_sch import TimeSchedule


app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Roles(str,Enum):
    candidate = "candidate"
    interviewer = "interviewer"

class Schedules_lst():
    def __init__(self,id=None,roles=None,dates_and_times=[]):
        self.id = id
        self.roles = roles
        for slots in dates_and_times:
            dates_and_times = datetime.strptime(slots,'%d/%m/%Y %H:%M')
        self.dates_and_times=dates_and_times.append(slots)
    #def schedules(self,dates_and_times):
    #    for slots in dates_and_times:
    #        datetime.strptime(slots,'%d/%m/%Y %H:%M')
    #        self.dates_and_times.append(slots) 
        
    #    return self.dates_and_times

        

class User(BaseModel):
    #id: Optional[UUID]=uuid4()
    id: int
    first_name: str
    last_name: str
    middle_name: Optional[str]
    email: str
    roles: Roles
    

    class Config:
            orm_mode = True    

class Schedules(BaseModel):
    #id: int
    slots: List[str]
    
      
    class Config:
            orm_mode = True 

class Slots(BaseModel):
    id: int
    user_id: int
    roles: str
    slots: List[str]

    class Config:
            orm_mode = True 

#Retrieve one user
def get_user(db: Session, user_id: int):
    return db.query(models.DBUser).where(models.DBUser.id == user_id).first()

#retrieve one user -call
@app.get('/user/{user_id}')
def get_user_view(user_id: int, db: Session = Depends(get_db)):
    return get_user(db, user_id)

#Retrieves all users
def get_users(db: Session):
    return db.query(models.DBUser).all()

#Retrieve all users -call
@app.get('/user/', response_model=List[User])
def get_user_view(db: Session = Depends(get_db)):
    return get_users(db)

#Create a new user
def create_user(db: Session, user: User):
    db_user = models.DBUser(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user
#Create a new user-call
@app.post('/user/', response_model = User)
def create_user_view(user: User, db: Session = Depends(get_db)):
    db_user = create_user(db, user)
    return db_user

def delete_user(db: Session, user_id: int):
    user =  get_user(db,user_id)
    if user:
        db.delete(user)
        db.commit()
        return

#delete an user-call
@app.delete('/user/{user_id}')
async def delete_user_view(user_id: int,db: Session = Depends(get_db)):
    return delete_user(db,user_id)

#update an user-function and call
@app.put("/user/{user_id}")
async def update_user_view(user_id: int,user: User, db: Session = Depends(get_db)):
   user_model = db.query(models.DBUser).filter(models.DBUser.id == user_id).first() 
   if user_model is None:
    raise HTTPException(
        status_code=404,detail=f"ID{user_id}: Does not exist"
    )
   user_model.first_name = user.first_name
   user_model.last_name = user.last_name
   user_model.middle_name = user.middle_name
   user_model.email = user.email
   user_model.roles = user.roles

   db.add(user_model)
   db.commit()
   return user      

#get a schedule-function
def get_slots(user_id: int,db: Session):
    return db.query(models.DBSchedule).where(models.DBSchedule.id == user_id).first()
#get a schedule-function-call

@app.get('/slots/{user_id}/')
async def get_schedules_view(user_id: int,db:Session=Depends(get_db)):
     return get_slots(user_id,db)


#post a schedule-function
def post_schedule(user_id: int,schedules:Schedules,db:Session):
    user=get_user(db,user_id)
    for slot in schedules.slots:
        slot_model = models.DBSchedule()
        slot_model.id = str(uuid4())    
        slot_model.user_id = user.id# db.query(models.DBUser.id).where(models.DBUser.id==user_id).first()
        slot_model.roles = user.roles#db.query(models.DBUser.roles).where(models.DBUser.id==user_id).first()
        slot_model.slots = slot
        db.add(slot_model)
    db.commit()
    db.refresh(slot_model)

#post a schedule-call
@app.post("/user/{user_id}/slots/",response_model=Slots)
async def post_schedules_view(user_id: int,schedules:Schedules, db: Session=Depends(get_db)):
    user_slots = post_schedule(user_id,schedules,db)
    return user_slots

#root
@app.get('/')
async def root(alan: int = 0):
    return {'message': 'Killing me softly!','alan': alan }
'''
#create a Login:
#https://www.youtube.com/watch?v=xZnOoO3ImSY&ab_channel=IanRufus
@app.post("/login")
def login():
    return{}

@app.get("/unprotected")
def unprotected():
    return{}

@app.get("/protected")
def protected():
    return{}        

#The calendar part

@app.get("/calendars/{id}")
def calendar(id: int ,test: str, definition: str ):
    return {"id": id,"first word": test,"2nd word": definition }    
'''
#@app.paste("calendars/{id}/{role}/{}")
#def add_schedule("id": id, date: str, time_start: str, event_duration: int ):
#    return {}

"""Old version
@app.get("/user/{user_name}{user_email}{user_role}")
def read_userx(user_name: str,user_email: str, user_role: str):
    user1 = userx(user_name,user_email,user_role)
    return("the stats of the user are:"+user1.name,user1.email,user1.role)

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
"""




