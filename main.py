#libraries
from fastapi import FastAPI,HTTPException,Depends,Query
from pydantic import BaseModel,Field
from uuid import UUID, uuid4
from typing import Union,List,Optional
from enum import Enum
from datetime import datetime
from sqlalchemy.orm import Session
#other files
import models
import add_database
import methods
#from agenda_sch import TimeSchedule


app = FastAPI()

add_database.Base.metadata.create_all(bind=add_database.engine)

def get_db():
    db = add_database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

#root
@app.get('/')
async def root(alan: int = 1):
    return {'message': 'Interviews Scheduler','alan': "Alan Jorge Alves do Carmo: v. {alan}" }

#----------------END POINTS--------------------------------------------------------
#Create a new user-call
@app.post('/users/', response_model = methods.User)
def create_user_view(user: methods.User, db: Session = Depends(get_db)):
    db_user = methods.create_user(user,db)
    return db_user


#retrieve one user -call
@app.get('/users/{user_id}')
def get_user_view(user_id: str, db: Session = Depends(get_db)):
    methods.user_exists(user_id,db)
    return methods.get_user(user_id,db)


#Retrieve all users -call
@app.get('/users/')
def get_all_users_view(db: Session = Depends(get_db)):
    if db.query(models.DBUser).first() is None:
        raise HTTPException(
        status_code=400,detail=f"Table DBUser has no entries."
    )
    return methods.get_users(db)
             
            


#update an user-function and call
@app.put("/users/{user_id}")
async def update_user_view(user_id: str,user: methods.User, db: Session = Depends(get_db)):
   user_model = db.query(models.DBUser).filter(models.DBUser.id == user_id).first()
   if user_model is None:
    raise HTTPException(
        status_code=404,detail=f"ID {user_id} does not exist"
    )
   user_model.first_name = user.first_name
   user_model.last_name = user.last_name
   user_model.middle_name = user.middle_name
   user_model.email = user.email
   user_model.role = user.role

   db.add(user_model)
   db.commit()
   return user   


#delete an user-call
@app.delete('/users/{user_id}')
async def delete_user_view(user_id: str,db: Session = Depends(get_db)):
    methods.user_exists(user_id,db)
    return methods.delete_user(db,user_id)

#post all the time-slots of an user -call
@app.post("/users/{user_id}/slots/",response_model=List[str])
async def post_slots_user_view(user_id: str,schedules:methods.Slots, db: Session=Depends(get_db)):
    methods.user_exists(user_id,db)
    try: user_slots = methods.post_slots_user(user_id,schedules,db)
    except ValueError: 
        raise HTTPException(
        status_code=400,detail=f"Slots are not in correct format: %d%m%y %H:%M")
    return user_slots


#get all the time-slots of an user schedule-call
@app.get('/users/{user_id}/slots/')
async def get_slots_user_view(user_id: str,db:Session=Depends(get_db)):
    methods.user_exists(user_id,db)
    methods.slots_exists(user_id,db) 
    return methods.get_slots(user_id,db)

#get all the time slots for all users
@app.get('/users/slots/')
async def get_all_slots_view(db:Session=Depends(get_db)):
     if db.query(models.DBSlots).first() is None:
        raise HTTPException(
        status_code=400,detail=f"Table DBSlots has no entries."
    )
     return methods.get_all_slots(db)

#get all the time slots for a given role
@app.get('/users/slots/{role}')
async def get_slots_role_view(role: str,db:Session=Depends(get_db)):
    try: role not in methods.Roles(role)
    except ValueError:  
        raise HTTPException(
        status_code=400,detail=f"{role}: Is not a valid role."
    )
    return methods.get_slots_by_role(role,db)     

#delete time slots of an user:
@app.delete('/users/{user_id}/slots/')
async def delete_slots_view(user_id: str,db: Session = Depends(get_db)):
    methods.user_exists(user_id,db)
    methods.slots_exists(user_id,db)  
    return methods.delete_slots(user_id,db)

#update time-slots for an user
@app.put("/users/{user_id}/slots/")
async def update_slots_view(user_id: str,slots: methods.Slots, db: Session = Depends(get_db)):
    methods.user_exists(user_id,db)
    methods.slots_exists(user_id,db) 
    return methods.update_slots(user_id,slots,db)
    
    
   
   
     
#get the schedules of a candidate and his/her interviewers
'''Should retrieve a list of schedules with:
-Id of the candidate
-first name and last name of the candidate
-slots matched
-name of the interviewers
'''
#get the schedules of a given user for all interviewers
'''
@app.get('/users/{user_id}/schedules/')
async def get_candidate_schedules_view(user_id: str,db:Session=Depends(get_db)):
    return methods.get_candidate_schedules(user_id,db)
'''
#If we want too query also the interviewers list

@app.get('/users/{user_id}/schedules/')
async def get_candidate_schedules_view(user_id: str,interviewers: Union[List[str],None]=Query(default=None),db:Session=Depends(get_db)):
    #routines to check if the id used for candidate and interviewers exist and corresponds to what they should
    candidate = methods.get_user(user_id,db)
    user_model = db.query(models.DBUser).filter(models.DBUser.id == user_id).first()
    if user_model is None:
      raise HTTPException(
        status_code=404,detail=f"ID of candidate {user_id} does not exist"
    )
    if candidate.role!="candidate":
        raise HTTPException(status_code=400,detail=f"{user_id}: is not the ID of a candidate.")
    for interviewer in interviewers:
        interviewer = methods.get_user(interviewer,db)
        if interviewer is None:
          raise HTTPException(
        status_code=404,detail=f"ID of interviewer: {user_id} does not exist"
    ) 
        elif interviewer.role!="interviewer":
                raise HTTPException(status_code=400,detail=f"{interviewer.id}: is not the ID of an interviewer.")
    return methods.get_candidate_schedules(user_id,interviewers,db)






    




