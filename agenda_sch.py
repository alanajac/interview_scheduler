from fastapi import APIRouter
from models import User,Roles
from datetime import date,timedelta
from typing import Union,List
from pydantic import BaseModel
from enum import Enum



class TimeSchedule(BaseModel):
    id: User.id
    date: str
    start_time: str
    duration: int


#@route_calendar.post("/create")
#async def create(request: Request):
#    pass

