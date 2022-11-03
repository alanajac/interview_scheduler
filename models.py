from typing import Optional,List
from pydantic import BaseModel
from uuid import UUID, uuid4
from enum import Enum
from datetime import datetime,timedelta
from agenda_sch import TimeSchedule

#class RoleChecker:
#    def __init__(self, Roles: List):
#        self.Roles = Roles

#    def __call__(self, user: User = Depends(get_current_active_user)):
#        if user.roles not in self.Roles:
#            logger.debug(f"User with role {user.roles} not in {self.Roles}")
#            raise HTTPException(status_code=403, detail="Operation not permitted")

#allow_create_resource = RoleChecker(["interviewer", "candidate"])

class Roles(str,Enum):
    candidate = "candidate"
    interviewer = "interviewer"
    

class User(BaseModel):
    id: Optional[UUID]= uuid4()
    first_name: str
    last_name: str
    middle_name: Optional[str]
    email: str
    roles: Roles
#    availability: List[TimeSchedule]


class UserUpdateRequest(BaseModel):
    id: Optional[UUID]=uuid4()
    first_name: Optional[str]
    last_name: Optional[str]
    middle_name: Optional[str]
    roles: Optional[str]
    availability: Optional[List[TimeSchedule]]


#Fake database to store users.




