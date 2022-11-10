# Interview Scheduler 
https://github.com/alanajac/interview_scheduler
 Alan Jorge Alves do Carmo, 09/11/2022.

[comment]: <> (A estrutura: dá um parágrafo ou dois de introdução, depois explica cada um dos endpoints com:
1- endpoint
2- parâmetros obrigatórios e opcionais
3- retornos esperados
4- tipos de erros que podem ser lançados)

[comment]: <> (Depois tu cria uma seção chamada arquitetura e explica tuas decisões (por que o FastApi, por que o SqlAlchemy, por que o MySql, como os arquivos estão separados)
##1. Overview

This is the documentation for a Interview Scheduler API developed by Alan Jorge Alves do Carmo, 09/11/2022.

**Assignment:**

There may be two roles that use this API, a candidate and an interviewer. A typical scenario is when:


An interview slot is a 1-hour period of time that spreads from the beginning of any hour until the beginning of the next hour. For example, a time span between 9am and 10am is a valid interview slot, whereas between 9:30am and 10:30am is not.


Each of the interviewers sets their availability slots. For example, the interviewer Ines is available next week each day from 9am through 4pm without breaks and the interviewer Ingrid is available from 12pm to 6pm on Monday and Wednesday next week, and from 9am to 12pm on Tuesday and Thursday.


Each of the candidates sets their requested slots for the interview. For example, the candidate Carl is available for the interview from 9am to 10am any weekday next week and from 10am to 12pm on Wednesday.


Anyone may then query the API to get a collection of periods of time when it’s possible to arrange an interview for a particular candidate and one or more interviewers. In this example, if the API queries for the candidate Carl and interviewers Ines and Ingrid, the response should be a collection of 1-hour slots: from 9am to 10am on Tuesday, from 9am to 10am on Thursday.

##2. Stack and Installation

Python 3.8>
Sqlite3 

Libraries: 
**Installating of libraries:***
pip3 <name of the library>
Libraries list:
-Fastapi (framework)
-sqlalchemy
-pydantic
-typing
-datetime
-os
-uuid
-enum


##3. EndPoints
All the endpoints can be checked and tested at: http://localhost:8000/docs
Below follows a short description of each Endpoint of the API.

###3.1 User Endpoints

Endpoints related to Operations to User.

####3.1.1 GET  /users/
Response: List all the Users stored in the database as well as their data, which have the fields: id, first name, last name, email and role(candidate or interviewer). Does not require parameters.
In case there are no Users in the Table, it returns an empty List. In this Endpoint it is also possible to retrieve the ID number of each stored in the database.

####3.1.2 POST /users/

Response: Adds an user to the database. It has as mandatory parameter the request body:
{
  "first_name": "string",
  "last_name": "string",
  "middle_name": "string",
  "email": "string",
  "role": "candidate/interviewer"
}
where first_name, last_name, email and role are required. role should be either "candidate" or "interviewer". The ID from each user can be retrieved from the Endpoint GET /users/ (3.1.1 GET /users/).
In case an input of that field is neither candidate or interviewer, the API raises an Error: "value is not a valid enumeration member; permitted: 'candidate', 'interviewer'"

####3.1.3 GET /users/{used_id}
Response: Gets the data of an existent User in the data using as rqeuired input parameter the ID of the User(string). Response is in the format of a List of Strings.
If there is no User with that ID, it returns an Exception: "ID: {user_id} does not exist"

####3.1.4 PUT /users/{user_id}
Response: Update the data of an existent User by inputing as a required parameters the ID of the User as a string. If there is no User with that ID, it returns an Exception: "ID: {user_id} does not exist". For the update of the data the required equest body is:
{
  "first_name": "string",
  "last_name": "string",
  "middle_name": "string",
  "email": "string",
  "role": "candidate/interviewer"
}
which follows the same rules from 3.1.2.


####3.1.5 DELETE /users/{user_id}

Response: Deletes from the database all the data of a given User with ID input as a required parameter. If there were time-slots stored and associated to that user, it is also erased from the database.

###3.2 Time-Slots Endpoints

Endpoints related to Operations to the Time-Slots of the Users.

####3.2.1 GET /users/{user_id}/slots
Response: Giving the parameter ID of the User (String)as input, retrieves all the time-slots stored by the User ID. If there is no time slots associated, it returns an empty List. If there is no User associated to that ID, it raises an Excetpion: ID: {user_id} does not exist".

####3.2.3 POST /users/{user_id}/slots
Response: Store in the database the available time-slots of an User for an interview. It requires as mandatory parameter the ID of the User which you want to associate the time-slots.
The request body is a List of Strings with format:
{
  "slots": [
    "string"
  ]
}
Each instance of the List should be written in the string format: 'dd/mm/yy hh:00'. The time-slots have one hour of interval. So each time-slot store the initial time of the interview.
Example:
{
  "slots": [
	    "10/11/22 9:00","10/11/22 11:00","10/11/22 12:00","11/11/22 9:00","11/11/22 10:00","12/11/22 14:00","12/11/22 15:00","13/11/22 9:00"
	    ]
}
If the format is not correct, the API raises an Exception: 
  
####3.2.2 PUT /users/{user_id}/slots
Response: Update the data of the time-slots of an User. It has the ID of the User as required parameter. Also, the time-slots of the User. The Client has to introduce the new available timme-slots. The past ones will be erased from database.
The format of the request body is the same as in 3.2.1.


####3.2.5 GET users/slots/
Response: Get all the time-slots for all users. Does not require any parameter. It returns an empty list if there are no instances in the database.

####3.2.6 GET /users/slots/{role}
Response: It gives all the time-slots for all user of a specific role: Candidate or Interviewer. It has as required mandatory parameter, the string "candidate" or "interviewer".
If an input parameter is not "candidate" or "interviewer" the API raises an Exception: "{role}: Is not a valid role."


####3.2.4 DELETE /users/{user_id}/slots
Response: Deletes all the time-slots associated to an existent User. Requires as mandatory parameter the ID of an existent user. If the input ID is not associated to an user, the API returns an Exception: "ID: {user_id} does not exist".
If there are no time-slots associated to an existent input ID, it raises an Exception:
"There are no time slots for ID: {user_id}".

###3.3 Schedules Endpoint
####3.3.1 GET /users/{user_id}/schedules/
Response: Returns a collection of coincident time-slots for a given candidate and one or more interviewers.
Requires as mandatory parameter the ID of an existent User with a role of "candidate". If the user is not a candidate, the API raises an Exception: ID of candidate {user_id} does not exist". Requires also, as path, the ID of one or more interviewers. If there are no interviewers associated to that ID, it raises the Exception: is not the ID of an interviewer.

##4. Architecture

For the project I decided to use Python, since is one of the most versatile and simple programming languages avaialable, with several useful libraries. 

For the Framework I used FastApi since it issimple and together with OpenApi provides an Endpoint /docs/  with an interface that shows the architecture of the Endpoints. I also used uvicorn, an ASGI web server implementation for Python, for the creation of a local webserver.
For the local database I used Sqlite3 and for the connection of the Framework and for the connection of the database with the Framework I used SQLAlchemy. The choice of a local database was for the reason of simplicity. In a later version of the project it would include the connection to SQLServers.

The Architecture of the API is structured by 3 main files:

#### main.py
main.py is where the API runs. It also contains the database connection, the endpoints of the API and the description of the Endpoints.

#### add_database.py
In add_database.py there is the characteristics of the Local database in sqlite3 and the engine and URL of the database.

#### methods.py
In methods.py there are described the helper methods of the API, which are of three kinds: The error handling methods, the user methods and the time-slots and schedules methods.

#### models.py
In models.py the models of the two tables which belong to the database are described.

The choice of the architecture had as objective organize and separate the methods from the endpoints of the API. In order to not mix the database and their models with the methods and endpoints, it was also separated from the other files. The reason for that would be for an easy modification or addition of New Models and the future connection with SQLServers.


##5. A Test Example Tutorial

In this section I provide a step-by-step tutorial of how to use the API to obtain a collection of time-slots for an interview of a candidate by one or more interviewers, by inputing their time-slots availability according to the description in the Section 1.
There is also the option of using an already filled database with some data. To check the commands without the need of adding the data to it.

The file support_file.dat contains data to be used in the step-by-step procedure below.
In the folder /sqlite/ there is already a filled database which are already loaded and can be used straight to get the results. If you prefer to do that test instead, go straight to **section 5.4**


####5.1. Starting the OpenApi Interface

First step, is to begin the uvicorn webserver with the command:
From the main directory of the project, give the command:

**uvicorn main:app --reload**
After that, open the browser and the address:
http://localhost:8000/docs/

####5.2 Inputing Users.
In the User section, open the  POST /user/{} endpoint. Click on tryout.
Open the file support_file.dat and copy the User fields:
{
  "first_name": "Joãozinho",
  "last_name": "Inverno",
  "middle_name": "",
  "email": "johnny@winter.com",
  "role": "interviewer"
}
Poste it in the Request body field and click on Execute. 
Do the same for two other users:
{
  "first_name": "Roberto",
  "last_name": "Planta",
  "middle_name": "",
  "email": "led@zeppelin.com",
  "role": "interviewer"
}
and:
{
  "first_name": "Alan",
  "last_name": "Carmo",
  "middle_name": "",
  "email": "alan@email.com",
  "role": "candidate"
}
You can now check the ID number of the Users and the data of the Users in the Endpoint:
GET /users/ Get all Users View

####5.3 Inputing time-slots for each User.

From the GET /users/ Get all Users View copy the ID number to the first User.
Go to the POST /users/{user_id}/slots/ Endpoint. Click on tryout.
Open again the file support_files.dat, and copy the following data:
{
  "slots": [
    "10/11/22 10:00","10/11/22 11:00","11/11/22 12:00","11/11/22 13:00","11/11/22 10:00","12/11/22 15:00","12/11/22 15:00","13/11/22 9:00"
  ]
}
Poste it in the Response body, and click "Execute".
Do the same for the other two ID numbers from the other users and the following time-slots:
{
  "slots": [
    "10/11/22 15:00","10/11/22 16:00","11/11/22 10:00","11/11/22 11:00","11/11/22 12:00","12/11/22 10:00","12/11/22 15:00","13/11/22 8:00","13/11/22 9:00"
  ]
}
{
  "slots": [
	    "10/11/22 9:00","10/11/22 11:00","10/11/22 12:00","11/11/22 9:00","11/11/22 10:00","12/11/22 14:00","12/11/22 15:00","13/11/22 9:00"
	    ]
}
You can check that the time-slots were input using two GET Endpoints:
GET /users/{user_id}/slots -to check the slots of time for a given user ID.
GET /users/slots - to check all the slots of time for all users.

####5.4 Get the Matched Schedules from candidate and interviewer(s)

Finally, with all the data input, go to the Endpoint:
GET /users/{user_id}/schedules/
Insert in the user_id field, the id number of the candidate inserted before, that can be retrieved in the GET /users/ Get all Users View - endpoint.

In the field interviewers, add the ID number of one or more interviewers which are in our database.
Then, press Execute.
The API should return a list of Schedules in ascending order from the earlier to the latest time and date. A schedule which matches both interviewers and the candidate should be next to each other, being easy to recognize the times in which we have a match of the time slots of all Users chosen.


##6. Limitations and Next Steps

The project described above is able to solve the assignment described in Section 1. There are a few limtations and improvements which would make the API more efficient and scalable.Hereby I detail some of those aspects.
 
####6.1 - Time and Date Limitations
 Even though we described the string format as 'dd/mm/hh H:00', it is actually possible to write the minutes in the format. A simple modification to insert only the H and transform the H to a H:00 string format would be enough to solve the issue.

 Also, other factors can be used in consideration, such as the TIMEZONE where the candidates and interviewers are. In this 

####6.2 -Input User limitations
It is actually possible to fill all the fields of the User as blank. We should change that for making mandatory at least the fields: first_name, last_name, email, role.


####6.3 Final Schedules Output

The final Schedules output order in time the candidate's time slots available that match one or more interviewers' time slots. A prefferable solution would select a list of the Users (candidate and interviewer(s)) in a list of IDs 

####6.4 Connection to an SQL Server

In further versions we intend to connect the API with SQLServers instead of using a local database.

####6.5 Authentication

In this first version, everyone can change the time slots and information of users, candidates and interviewers. That is not a safe solution when we have many users accessing it. For that, the authentication for the different roles providing different access levels for each.


