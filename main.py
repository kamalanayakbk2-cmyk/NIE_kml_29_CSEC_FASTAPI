```python
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from pymongo import MongoClient

# ==========================================
# FASTAPI APP
# ==========================================

app = FastAPI(
    title="Ticket Management System",
    version="1.0.0"
)

# ==========================================
# CORS
# ==========================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================
# MONGODB
# ==========================================

MONGO_URL = "mongodb://127.0.0.1:27017"

client = MongoClient(MONGO_URL)

db = client["service_ticket_db"]

users_collection = db["users"]
tickets_collection = db["tickets"]


# ==========================================
# MODELS
# ==========================================

class UserCreate(BaseModel):
    username: str
    password: str


class TicketCreate(BaseModel):
    title: str
    description: str
    category: str
    status: str


# ==========================================
# HOME
# ==========================================

@app.get("/")
def home():
    return {
        "message": "Ticket Management API is working!"
    }


# ==========================================
# REGISTER USER
# ==========================================

@app.post("/users")
def create_user(user: UserCreate):

    # Check if username already exists
    existing_user = users_collection.find_one(
        {"username": user.username}
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    # Create user
    new_user = {
        "username": user.username,
        "password": user.password
    }

    result = users_collection.insert_one(new_user)

    return {
        "message": "User created successfully",
        "username": user.username,
        "id": str(result.inserted_id)
    }


# ==========================================
# LOGIN
# ==========================================

@app.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends()
):

    user = users_collection.find_one(
        {
            "username": form_data.username,
            "password": form_data.password
        }
    )

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    return {
        "message": "Login successful",
        "access_token": "login-token",
        "token_type": "bearer",
        "username": form_data.username
    }


# ==========================================
# CREATE TICKET
# ==========================================

@app.post("/tickets")
def create_ticket(ticket: TicketCreate):

    ticket_data = {
        "title": ticket.title,
        "description": ticket.description,
        "category": ticket.category,
        "status": ticket.status
    }

    result = tickets_collection.insert_one(ticket_data)

    return {
        "message": "Ticket created successfully",
        "id": str(result.inserted_id),
        "title": ticket.title,
        "description": ticket.description,
        "category": ticket.category,
        "status": ticket.status
    }


# ==========================================
# GET ALL TICKETS
# ==========================================

@app.get("/tickets")
def get_tickets():

    tickets = []

    for ticket in tickets_collection.find():

        tickets.append(
            {
                "id": str(ticket["_id"]),
                "title": ticket["title"],
                "description": ticket["description"],
                "category": ticket["category"],
                "status": ticket["status"]
            }
        )

    return tickets
```
