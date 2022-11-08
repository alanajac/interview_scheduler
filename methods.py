from sqlalchemy.orm import Session,aliased
from sqlalchemy import and_
import models
from typing import Union,List,Optional
from uuid import UUID, uuid4
from enum import Enum
from pydantic import BaseModel,Field
from datetime import datetime

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
    role: Roles


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
    role: str
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

#Helper method: String to datetime:
def string_to_datetime(date: str):
     return datetime.strptime(date,"%d/%m/%y %H:%M")

#-------------------------USER TABLE METHODS -------------------------------------------------------
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
    db_user.role= user.role
    db.add(db_user)
    db.commit()
    #db.refresh(db_user)

    return db_user

#delete user - method
def delete_user(db: Session, user_id: str):
    user =  get_user(db,user_id)
    if user:
        db.delete(user)
        db.commit()
        return
#------------------------TIME SLOTS TABLE METHODS ---------------------------------------------
#get all the slots of one user-method
#post slots for a given user- method
def post_slots_user(user_id: str,schedules:Slots,db:Session):
    #datetime_slot=[string_to_datetime(schedules.slots) for slot in schedules.slots]
    user=get_user(db,user_id)
    for slot in schedules.slots:
        datetime_slot =string_to_datetime(slot)
        slot_model = models.DBSlots()
        slot_model.id = str(uuid4())    
        slot_model.user_id = user.id
        slot_model.role = user.role
        slot_model.slots = datetime_slot
        db.add(slot_model)
        db.commit()
    
    return schedules.slots


def get_slots(user_id: str,db: Session):
    return db.query(models.DBSlots).where(models.DBSlots.user_id == user_id).all()


#get all the time slots of all users - method
def get_all_slots(db:Session):
    return db.query(models.DBSlots).all()


#Update all the time slots of an user
def update_slots(user_id: str,slots:Slots,db:Session):
    delete_slots(user_id,db)
    return post_slots_user(user_id,slots,db) 

#delete all time slots of an user  - method
def delete_slots(user_id: str,db: Session):
    for slot in db.query(models.DBSlots).filter(models.DBSlots.user_id==user_id).all():
        db.delete(slot)
    db.commit()
    return

#get all the time slots for a given role - method
def get_slots_by_role(role_name: str,db:Session):
    return db.query(models.DBSlots).where(models.DBSlots.role== role_name).all()


'''
  

select c.user_id as "candidate id", u.first_name "candidate name", u.last_name " candidate surname",i.user_id as "interviewer id",u2.first_name as "interviewer name", c.slots as "time slots"
from Schedules c 
inner join Users u on c.user_id = u.id and u.id = "1582721e-625c-4f70-97cc-9eb17a2810ff"
inner join Schedules i on c.slots = i.slots and i.role = "interviewer" 
inner join Users u2 on u2.id = i.user_id;
#columns should be:
c.user_id as "candidate id" - DBSlots_in.user_id ok
u.first_name "candidate name" -  DBUser_in.first_name ok
u.last_name " candidate surname" -  DBUser_in.last_name ok
i.user_id as "interviewer id" - DBSlots_out.user_id
u2.first_name as "interviewer name" DBUser_out.first_name
c.slots as "time slots" DBSlots_in.slots
DB_
'''
#Query to get the schedules between candidate and interviewers  -one candidate, all interviewers
#it works!
'''
def get_candidate_schedules(user_input: str,db:Session):
    DBSlots_in = aliased(models.DBSlots)
    DBSlots_out = aliased(models.DBSlots)
    DBUser_in = aliased(models.DBUser)
    DBUser_out = aliased(models.DBUser)
    #3rd attempt
    
    return db.query(DBSlots_in.user_id.label("candidate id"),DBUser_in.first_name.label("candidate name"),DBUser_in.last_name.label("candidate surname"),DBSlots_out.user_id.label("interviewer id"),DBUser_out.first_name.label("interviewer name"),DBSlots_in.slots.label("time slots")).select_from(DBSlots_in) \
    .join(DBUser_in,and_(DBSlots_in.user_id == DBUser_in.id,DBUser_in.id==user_input))\
    .join(DBSlots_out,and_(DBSlots_in.slots == DBSlots_out.slots,DBSlots_out.role == "interviewer"))\
    .join(DBUser_out,DBUser_out.id==DBSlots_out.user_id).order_by(DBSlots_in.slots).all()

#List comprehensions -work-query
    result = [(db.query(DBSlots_in.user_id.label("candidate id"),DBUser_in.first_name.label("candidate name"),DBUser_in.last_name.label("candidate surname"),DBSlots_out.user_id.label("interviewer id"),DBUser_out.first_name.label("interviewer name"),DBSlots_in.slots.label("time slots")).select_from(DBSlots_in) \
    .join(DBUser_in,and_(DBSlots_in.user_id == DBUser_in.id,DBUser_in.id==user_input))\
    .join(DBSlots_out,and_(DBSlots_in.slots == DBSlots_out.slots,DBSlots_out.user_id == interviewer)).join(DBUser_out,DBUser_out.id==DBSlots_out.user_id).order_by(DBSlots_in.slots)).all() for interviewer in interviewers]
'''    
#Query to get the schedules between candidate and a list of interviewers
     
def get_candidate_schedules(user_input: str,interviewers:List[str],db:Session):
    print(interviewers)
    DBSlots_in = aliased(models.DBSlots)
    DBSlots_out = aliased(models.DBSlots)
    DBUser_in = aliased(models.DBUser)
    DBUser_out = aliased(models.DBUser)
    
    result = (db.query(DBSlots_in.user_id.label("candidate id"),DBUser_in.first_name.label("candidate name"),DBUser_in.last_name.label("candidate surname"),DBSlots_out.user_id.label("interviewer id"),DBUser_out.first_name.label("interviewer name"),DBSlots_in.slots.label("time slots")).select_from(DBSlots_in) \
    .join(DBUser_in,and_(DBSlots_in.user_id == DBUser_in.id,DBUser_in.id==user_input))\
    .join(DBSlots_out,and_(DBSlots_in.slots == DBSlots_out.slots,DBSlots_out.user_id.in_(interviewers))).join(DBUser_out,DBUser_out.id==DBSlots_out.user_id).order_by(DBSlots_in.slots)).all()

    return result
    
'''    #3rd attempt
    result = db.query(DBSlots_in.user_id.label("candidate id"),DBUser_in.first_name.label("candidate name"),DBUser_in.last_name.label("candidate surname"),DBSlots_out.user_id.label("interviewer id"),DBUser_out.first_name.label("interviewer name"),DBSlots_in.slots.label("time slots")).select_from(DBSlots_in) \
    .join(DBUser_in,and_(DBSlots_in.user_id == DBUser_in.id,DBUser_in.id==user_input))\
    .join(DBSlots_out,and_(DBSlots_in.slots == DBSlots_out.slots,DBSlots_out.user_id == 'a14076ca-5ee0-4995-b253-5d91240094ca')).join(DBUser_out,DBUser_out.id==DBSlots_out.user_id).order_by(DBSlots_in.slots).all()

    return result
'''
#comment
''' 
    return result
    result = [(db.query(DBSlots_in.user_id.label("candidate id"),DBUser_in.first_name.label("candidate name"),DBUser_in.last_name.label("candidate surname"),DBSlots_out.user_id.label("interviewer id"),DBUser_out.first_name.label("interviewer name"),DBSlots_in.slots.label("time slots")).select_from(DBSlots_in) \
    .join(DBUser_in,and_(DBSlots_in.user_id == DBUser_in.id,DBUser_in.id==user_input))\
    .join(DBSlots_out,and_(DBSlots_in.slots == DBSlots_out.slots,DBSlots_out.user_id == interviewer)).join(DBUser_out,DBUser_out.id==DBSlots_out.user_id).order_by(DBSlots_in.slots)).all() for interviewer in interviewers]
   

     #Using list comprehensions:
    #my_list = [param for param in iterable]
    Sane as: for char in 'hello':
                my_list.append(char)
    my_list = [char for char in 'hello']            
    hello-> our input list
    first char: ?-variable ->our expression?
    second_char: ?
    first char is an expression
    my_list = [expression for parameter in iterable]
'''