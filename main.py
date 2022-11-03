from typing import Union,List
from fastapi import FastAPI,HTTPException
from models import User,Roles,UserUpdateRequest
from uuid import UUID, uuid4
from agenda_sch import TimeSchedule
app = FastAPI()

#creating a test database of the Users
db: List[User] = [
    User(
        id=uuid4(),
        first_name = "Jamila",
        last_name = "Ahmed",
        roles=Roles.interviewer),
        #availability = [TimeSchedule.Schedule])
    User(
        id=uuid4(),
        first_name="Alan",
        last_name="Alves",
        roles=Roles.candidate)
        #availability = [TimeSchedule.Schedule])
]

#Register a new user
@app.post("/api/v1/users")
async def register_user(user: User):
    db.append(user)
    return {"user_id":user.id}


#We have to send our client the users:

@app.get("/api/v1/users")
async def fetch_users():
    return db

#Update the user
@app.put("/api/v1/users/{user_id}")
async def update_users(user_update: UserUpdateRequest,user_id: UUID):
    for user in db:
        if user.id == user_id:
            if user_update.first_name is not None:
                user.first_name=user_update.first_name
            if user_update.last_name is not None:
                user.last_name=user_update.last_name    
            if user_update.middle_name is not None:
                user.middle_name=user_update.middle_name
            if user_update.roles is not None:
                user.roles=user_update.roles        
        raise HTTPException(
            status_code = 404, detail=f"user with id:{user_id} does not exist"
        )


#Delete users
app.post("/api")
@app.delete("/api/v1/users({user_id}")
async def delete_user(user_id: UUID):
    for user in db: 
        if user.id ==user_id:
            db.remove(user)
            return
        raise   HTTPException(
            status_code=404,
            detail = f"user with id: {user_id} does not exists"
        )    
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

#@app.paste("calendars/{id}/{role}/{}")
#def add_schedule("id": id, date: str, time_start: str, event_duration: int ):
#    return {}

@app.get("/")
def read_root():
    return {"Interview Calendar": "Please write your name, email and if you are a candidate or interviewer."}
"""Old version
@app.get("/user/{user_name}{user_email}{user_role}")
def read_userx(user_name: str,user_email: str, user_role: str):
    user1 = userx(user_name,user_email,user_role)
    return("the stats of the user are:"+user1.name,user1.email,user1.role)

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
"""




