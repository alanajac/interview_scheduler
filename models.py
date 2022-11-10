#from uuid import UUID, uuid4
#import datetime
from pydantic import BaseModel,Field
#from typing import Union,List,Optional
#from agenda_sch import TimeSchedule
from add_database import Base
#from enum import Enum
from sqlalchemy import Column, String,ForeignKey,DateTime
from sqlalchemy.orm import relationship
#from add_database import engine
#from fastapi_utils.guid_type import GUID
#class RoleChecker:
#    def __init__(self, Roles: List):
#        self.Roles = Roles

#    def __call__(self, user: User = Depends(get_current_active_user)):
#        if user.roles not in self.Roles:
#            logger.debug(f"User with role {user.roles} not in {self.Roles}")
#            raise HTTPException(status_code=403, detail="Operation not permitted")



#allow_create_resource = RoleChecker(["interviewer", "candidate"])
class DBUser(Base):
    __tablename__ = 'Users'
    id = Column(String,primary_key=True,index=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    middle_name = Column(String(50))
    email = Column(String(50))
    role = Column(String)
    
    schedules = relationship("DBSlots", back_populates="user",cascade="all,delete,delete-orphan")

class DBSlots(Base):
    __tablename__ = 'Slots'
    id =  Column(String,primary_key=True,index=True )
    user_id = Column(String,ForeignKey("Users.id"))
    role = Column(String(50))
    slots = Column(DateTime)

    user = relationship("DBUser", back_populates="schedules",passive_deletes=True)#->Not necessary to this 
    



#class Schedules()    







