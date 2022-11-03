from fastapi import APIRouter
from typing import Union,List,Optional
from pydantic import BaseModel
from enum import Enum
from uuid import UUID, uuid4
from datetime import datetime


class Roles(str,Enum):
    candidate = "candidate"
    interviewer = "interviewer"

#class Schedules()
class Config:
    arbitrary_types_allowed = True
    
class Schedule():

    def __init__(self,id,roles):
        self.id = id
        self.roles = roles    

    def schedules(self,dates_and_times):
        for slots in dates_and_times:
            datetime.strptime(slots,'%d/%m/%Y %H:%M')
            self.dates_and_times.append(slots) 
        
        return self.dates_and_times

class User(BaseModel):
    id: Optional[UUID]= uuid4()
    first_name: str
    last_name: str
    middle_name: Optional[str]
    email: str
    roles: Roles
    schedule: Schedule



user1 = User(
        id=uuid4(),
        first_name = "Alan",
        last_name = "Alves",
        email = "alan.ajac@gmail.com",
        roles = Roles.interviewer,
        schedule =  [User.id,User.roles,['04/11/2022 9:00','04/11/2022 10:00','04/11/2022 11:00','04/11/2022 15:00','05/11/2022 12:00','05/11/2022 9:00']])
print(user1.schedule)




scheduled_days = ['04/11/2022 9:00','04/11/2022 10:00','04/11/2022 11:00','04/11/2022 15:00','05/11/2022 12:00','05/11/2022 9:00']
for dates in scheduled_days:
    datetime.strptime(dates,'%d/%m/%Y %H:%M')
print(scheduled_days)
