from sqlalchemy.orm import Session,aliased
from sqlalchemy import and_
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


class Slot_Table(BaseModel):
    id: str
    user_id: str
    roles: str
    slot: str

    class Config:
        orm_mode = True
              
      
class Schedules(BaseModel):
    id: str
    first_name: str
    last_name: str
    slot: str
    interviewer: str
    
    
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

#CHECK THESE OUT
#get all the time slots of all users
def get_all_slots(db:Session):
    return db.query(models.DBSchedule).all()
'''def get_all_slots(db:Session):
    all_slots = Slot_Table()
    for instance in models.DBSchedule:
        all_slots.id = models.DBSchedule.id 
        all_slots.user_id = models.DBSchedule.user_id
        all_slots.roles = models.DBSchedule.roles
        all_slots.slot = models.DBSchedule.slots
#    all_slots = db.query(models.DBSchedule).all()
    return all_slots
'''

#get all the time slots for a given role
def get_slots_by_role(role_name: str,db:Session):
    return db.query(models.DBSchedule).where(models.DBSchedule.roles== role_name).all()

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

'''
#Query to get the schedules between candidate and interviewers    

select c.user_id as "candidate id", u.first_name "candidate name", u.last_name " candidate surname",i.user_id as "interviewer id",u2.first_name as "interviewer name", c.slots as "time slots"
from Schedules c 
inner join Users u on c.user_id = u.id and u.id = "1582721e-625c-4f70-97cc-9eb17a2810ff"
inner join Schedules i on c.slots = i.slots and i.roles = "interviewer" 
inner join Users u2 on u2.id = i.user_id;
#columns should be:
c.user_id as "candidate id" - DBSchedule_in.user_id ok
u.first_name "candidate name" -  DBUser_in.first_name ok
u.last_name " candidate surname" -  DBUser_in.last_name ok
i.user_id as "interviewer id" - DBSchedule_out.user_id
u2.first_name as "interviewer name" DBUser_out.first_name
c.slots as "time slots" DBSchedule_in.slots
DB_
'''
def get_candidate_schedules(user_input: str,db:Session):
    DBSchedule_in = aliased(models.DBSchedule)
    DBSchedule_out = aliased(models.DBSchedule)
    DBUser_in = aliased(models.DBUser)
    DBUser_out = aliased(models.DBUser)
    #slots_user = get_slots(user_input,db)
    #user = get_user(db,user_input)
    #slots_interviewer=get_slots_by_role("interviewer",db)
    #get list of all the Schedules
       #3rd attempt
    return db.query(DBSchedule_in.user_id.label("candidate id"),DBUser_in.first_name.label("candidate name"),DBUser_in.last_name.label("candidate surname"),DBSchedule_out.user_id.label("interviewer id"),DBUser_out.first_name.label("interviewer name"),DBSchedule_in.slots.label("time slots")).select_from(DBSchedule_in) \
    .join(DBUser_in,and_(DBSchedule_in.user_id == DBUser_in.id,DBUser_in.id==user_input))\
    .join(DBSchedule_out,and_(DBSchedule_in.slots == DBSchedule_out.slots,DBSchedule_out.roles == "interviewer"))\
    .join(DBUser_out,DBUser_out.id==DBSchedule_out.user_id).order_by(DBSchedule_in.slots).all()
    
    #1st attempt
    #return db.query(DBSchedule_in).join(DBUser_in).filter(DBSchedule_in.user_id==DBUser_in.id).filter(DBUser_in.id==user_input).join(DBSchedule_out).filter(DBSchedule_out.slots == DBSchedule_in.slots).filter(DBSchedule_out.roles == "interviewer").join(DBUser_out).filter(DBUser_out.id==DBSchedule_out.user_id).with_entities(DBSchedule_in.user_id,DBUser_in.first_name,DBUser_in.last_name,DBSchedule_out.user_id,DBUser_out.first_name,DBSchedule_in.slots).all()
    
    #2nd attempt
    '''
    return db.query(DBSchedule_in.user_id,DBUser_in.first_name,DBUser_in.last_name,DBSchedule_out.user_id,DBUser_out.first_name,DBSchedule_in.slots).select_from(DBSchedule_in) \
    .join(DBUser_in).filter(DBSchedule_in.user_id == DBUser_in.id).filter(DBUser_in.id==user_input)\
    .join(DBSchedule_out).filter(DBSchedule_in.slots == DBSchedule_out.slots).filter(DBSchedule_out.roles == "interviewer")\
    .join(DBUser_out).filter(DBUser_out.id==DBSchedule_out.user_id).all()
    '''
 
    #get from several interviewers:
    '''
    for interviewer in list_interviewers:
        db.query(DBSchedule_in).join(DBUser_in).filter(DBSchedule_in.user_id==DBUser_in.id).filter(DBUser_in.id==user_input).join(DBSchedule_out).filter(DBSchedule_out.slots == DBSchedule_in.slots).filter(DBSchedule_out.user_id == interviewer).join(DBUser_out).filter(DBUser_out.id==DBUser_in.id).with_entities(DBSchedule_in.user_id,DBUser_in.first_name,DBUser_in.last_name,DBSchedule_out.user_id,DBUser_out.first_name,DBSchedule_in.slots).all()
    #db.query(models.DBSchedule,models.DBUser,models.DBSchedule).all()
    '''
    #db.query(models.DBSchedule).where(models.DBSchedule.user_id==user_id)  

