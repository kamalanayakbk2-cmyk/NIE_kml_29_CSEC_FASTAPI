DAY2- FASTAPI

what is fastAPI?

&#x20;  \*it has major framework they are starlette,pydantic

&#x20;  \*pydantic - it is library is use to data validation and serialization

&#x20;  \*-ASGI based python web development framework(Asynchronous Server Gateway Interface)

&#x20;

REST API-Standard for APIs (web services) development

python: Django,Flask



pyhton has asynchronous

NodeJS has libuy - event loop



starlette uvloop site on libuy

uvicorn runs the FastAPI (starlette)app-help to write the web development code.



\------------\*\*\*\*\*\*-------------

pip install fastapi,uvicorn

to check- pip show uvicorn

to check  the installation-pip list

to update the python -python.exe -m pip install --upgrade pip



**REASTAPI()**

&#x20; HTTP METHOD + url end point = API End point

&#x20; \* http method are called verbs

&#x20; \* url is called noun

**path operations:-**

POST/user

GET/users

GET/users/101

PUT/users/101

DELETE/users/101



**code:-**

from fastapi import FastAPI



app = FastAPI()



@app.get("/")

def home():

&#x20;   return {"message": "Enterprise IT Service Desk"}

**steps:- to run**

**step1:-**

copy the link and paste it chrome and add/ tickets and search or

right click the file and choose reveal file option

this is the one path



then change the link at last "docs" then swagger ui will display

**step2:- just run the link again in chrome**

@app.get("/tickets/{-id}")

def ticket\_read\_by\_id(:d : int):

&#x20;   return db\[id]



**HTTPEXception  :- to avoid the spelling mistake use this command**



GET	🟢 GET = Give me data	Read / fetch data

POST	🔵 POST = Put new data	Create new data   adding the id number in code

PUT	🟡 PUT = Update data	Update existing data

DELETE	🔴 DELETE = Remove data	Delete data  / number of the id in link

