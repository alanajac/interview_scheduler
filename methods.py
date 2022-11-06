from sqlalchemy.orm import Session
import models
from typing import Union,List,Optional
from uuid import UUID, uuid4
from enum import Enum
from pydantic import BaseModel,Field


class Roles(str,Enum):
    candidate = "candidate"
    interviewer = "interviewer"

class User(BaseModel):
    #id: Optional[UUID]=uuid4()
    #id: str
    first_name: str
    last_name: str
    middle_name: Optional[str]
    email: str
    roles: Roles


    class Config:
        orm_mode = True    


class Slots(BaseModel):
    #id: int
    slots: List[str]
    
    class Config:
        orm_mode = True    
      
class Slotss(BaseModel):
    id: int
    user_id: int
    roles: str
    slots: List[str]

    class Config:
        orm_mode = True 

class Schedules(BaseModel):
    id: str
    first_name: str
    last_name: str
    interviewer: str
    slot: str
    
    class Config:
        orm_mode = True


#Retrieve one user
def get_user(db: Session, user_id: str):
    return db.query(models.DBUser).where(models.DBUser.id == user_id).first()


#Retrieves all users
def get_users(db: Session):
    return db.query(models.DBUser).all()

#Create a new user
def create_user(db: Session, user: User):
    #db_user = models.DBUser(**user.dict())
    db_user = models.DBUser()
    db_user.id = str(uuid4())
    db_user.first_name = user.first_name
    db_user.last_name = user.last_name
    db_user.middle_name = user.middle_name
    db_user.email = user.email
    db_user.roles = user.roles
    db.add(db_user)
    db.commit()
    #db.refresh(db_user)

    return db_user

def delete_user(db: Session, user_id: str):
    user =  get_user(db,user_id)
    if user:
        db.delete(user)
        db.commit()
        return

#get all the slots of one user-function
def get_slots(user_id: str,db: Session):
    return db.query(models.DBSchedule).where(models.DBSchedule.user_id == user_id).all()

#post a schedule-function
def post_schedule(user_id: str,schedules:Slots,db:Session):
    user=get_user(db,user_id)
    for slot in schedules.slots:
        slot_model = models.DBSchedule()
        slot_model.id = str(uuid4())    
        slot_model.user_id = user.id
        slot_model.roles = user.roles
        slot_model.slots = slot
        db.add(slot_model)
        db.commit()
    
    return schedules.slots

def get_candidate_schedules_view(user_id: str,schedules: Schedules,db:Session):
    pass    

