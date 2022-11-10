#libraries
from fastapi import FastAPI,HTTPException,Depends,Query
from typing import Union,List
from sqlalchemy.orm import Session
#other files
import models
import add_database
import methods
#from agenda_sch import TimeSchedule
#from uuid import UUID, uuid4
#from enum import Enum
#from datetime import datetime
#from pydantic import BaseModel,Field

description = '''
This is the documentation for a Interview Scheduler API developed by Alan Jorge Alves do Carmo, 09/11/2022.

There may be two roles that use this API, a candidate and an interviewer. A typical scenario is when:


An interview slot is a 1-hour period of time that spreads from the beginning of any hour until the beginning of the next hour. For example, a time span between 9am and 10am is a valid interview slot, whereas between 9:30am and 10:30am is not.


Each of the interviewers sets their availability slots. For example, the interviewer Ines is available next week each day from 9am through 4pm without breaks and the interviewer Ingrid is available from 12pm to 6pm on Monday and Wednesday next week, and from 9am to 12pm on Tuesday and Thursday.


Each of the candidates sets their requested slots for the interview. For example, the candidate Carl is available for the interview from 9am to 10am any weekday next week and from 10am to 12pm on Wednesday.


Anyone may then query the API to get a collection of periods of time when it’s possible to arrange an interview for a particular candidate and one or more interviewers. In this example, if the API queries for the candidate Carl and interviewers Ines and Ingrid, the response should be a collection of 1-hour slots: from 9am to 10am on Tuesday, from 9am to 10am on Thursday.'''

tags_metadata = [
    {
        "name": "Users",
        "description": "Operations with users.",
    },
    {
        "name": "Time Slots",
        "description": "Operations with the time Slots for candidates and interviewers.",
        },
        {
            "name": "Scheduler",
            "description": "Determine the available Schedules for the Interview given a candidate and one or more Interviewers."

        }
    ,
]

app = FastAPI(title='Interview Scheduler',
description=description,
openapi_tags=tags_metadata,
version="0.0.1",
contact={
    "name": "Alan Jorge Alves do Carmo",
    "url": "https://github.com/alanajac/interview_scheduler",
    "email": "alan.ajac@gmail.com"
}
)


add_database.Base.metadata.create_all(bind=add_database.engine)

def get_db():
    db = add_database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

#root
@app.get('/')
async def root():
    return {'message': 'Interviews Scheduler','alan': "Alan Jorge Alves do Carmo: v.1" }

#----------------END POINTS--------------------------------------------------------
#Create a new user-call
@app.post('/users/', response_model = methods.User,tags=["Users"])
def create_user_view(user: methods.User, db: Session = Depends(get_db)):
    db_user = methods.create_user(user,db)
    return db_user


#retrieve one user -call
@app.get('/users/{user_id}',tags=["Users"])
def get_user_view(user_id: str, db: Session = Depends(get_db)):
    methods.user_exists(user_id,db)
    return methods.get_user(user_id,db)


#Retrieve all users -call
@app.get('/users/',tags=["Users"])
def get_all_users_view(db: Session = Depends(get_db)):
    if db.query(models.DBUser).first() is None:
        raise HTTPException(
        status_code=400,detail=f"Table DBUser has no entries."
    )
    return methods.get_users(db)
             
            


#update an user-function and call
@app.put("/users/{user_id}",tags=["Users"])
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
@app.delete('/users/{user_id}',tags=["Users"])
async def delete_user_view(user_id: str,db: Session = Depends(get_db)):
    methods.user_exists(user_id,db)
    return methods.delete_user(db,user_id)

#post all the time-slots of an user -call
@app.post("/users/{user_id}/slots/",response_model=List[str],tags=["Time Slots"])
async def post_slots_user_view(user_id: str,schedules:methods.Slots, db: Session=Depends(get_db)):
    methods.user_exists(user_id,db)
    try: user_slots = methods.post_slots_user(user_id,schedules,db)
    except ValueError: 
        raise HTTPException(
        status_code=400,detail=f"Slots are not in correct format: %d%m%y %H:%M")
    return user_slots


#get all the time-slots of an user schedule-call
@app.get('/users/{user_id}/slots/',tags=["Time Slots"])
async def get_slots_user_view(user_id: str,db:Session=Depends(get_db)):
    methods.user_exists(user_id,db)
    return methods.get_slots(user_id,db)

#get all the time slots for all users
@app.get('/users/slots/',tags=["Time Slots"])
async def get_all_slots_view(db:Session=Depends(get_db)):
     if db.query(models.DBSlots).first() is None:
        raise HTTPException(
        status_code=400,detail=f"Table DBSlots has no entries."
    )
     return methods.get_all_slots(db)

#get all the time slots for a given role
@app.get('/users/slots/{role}',tags=["Time Slots"])
async def get_slots_role_view(role: str,db:Session=Depends(get_db)):
    try: role not in methods.Roles(role)
    except ValueError:  
        raise HTTPException(
        status_code=400,detail=f"{role}: Is not a valid role."
    )
    return methods.get_slots_by_role(role,db)     

#delete time slots of an user:
@app.delete('/users/{user_id}/slots/',tags=["Time Slots"])
async def delete_slots_view(user_id: str,db: Session = Depends(get_db)):
    methods.user_exists(user_id,db)
    methods.slots_exists(user_id,db)  
    return methods.delete_slots(user_id,db)

#update time-slots for an user
@app.put("/users/{user_id}/slots/",tags=["Time Slots"])
async def update_slots_view(user_id: str,slots: methods.Slots, db: Session = Depends(get_db)):
    methods.user_exists(user_id,db)
    methods.slots_exists(user_id,db) 
    return methods.update_slots(user_id,slots,db)
    
    
   
   
     
#get the schedules of a candidate and his/her interviewers
'''Should retrieve a list of schedules with:
-Id of the candidate
-first name and last name of the candidate
-time slots matched
-name of the interviewers
'''
#get the schedules of a given user for all interviewers
'''
@app.get('/users/{user_id}/schedules/')
async def get_candidate_schedules_view(user_id: str,db:Session=Depends(get_db)):
    return methods.get_candidate_schedules(user_id,db)
'''
#Get the list of matched times-lots for an interview of the candidate and selected interviewers

@app.get('/users/{user_id}/schedules/',tags=["Scheduler"])
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






    




