
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
from bson import ObjectId

# App
app = FastAPI(title="Hospital support Request system")

# Database
URL = "mongodb://127.0.0.1:27017"

client = MongoClient(URL)

db = client["hospital_support_db"]
service_requests = db["service_requests"]


# Schema
class ServiceRequest(BaseModel):
    title: str
    description: str
    department: str
    status: str
    assigned_to: str


# Helper
def request_helper(doc):
    return {
        "id": str(doc["_id"]),
        "title": doc["title"],
        "description": doc["description"],
        "department": doc["department"],
        "status": doc["status"],
        "assigned_to": doc["assigned_to"]
    }


# CREATE
@app.post("/service-requests", status_code=201)
def create_request(payload: ServiceRequest):

    request_data = payload.model_dump()

    result = service_requests.insert_one(request_data)

    new_request = service_requests.find_one(
        {"_id": result.inserted_id}
    )

    return request_helper(new_request)


# READ ALL
@app.get("/service-requests")
def get_all_requests():

    docs = service_requests.find()

    return [request_helper(doc) for doc in docs]


# READ BY ID
@app.get("/service-requests/{id}")
def get_request(id: str):

    if not ObjectId.is_valid(id):
        raise HTTPException(
            status_code=400,
            detail="Invalid request ID"
        )

    doc = service_requests.find_one(
        {"_id": ObjectId(id)}
    )

    if not doc:
        raise HTTPException(
            status_code=404,
            detail="Service request not found"
        )

    return request_helper(doc)


# UPDATE
@app.put("/service-requests/{id}")
def update_request(id: str, payload: ServiceRequest):

    if not ObjectId.is_valid(id):
        raise HTTPException(
            status_code=400,
            detail="Invalid request ID"
        )

    result = service_requests.update_one(
        {"_id": ObjectId(id)},
        {"$set": payload.model_dump()}
    )

    if result.matched_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Service request not found"
        )

    updated_request = service_requests.find_one(
        {"_id": ObjectId(id)}
    )

    return request_helper(updated_request)


# DELETE
@app.delete("/service-requests/{id}")
def delete_request(id: str):

    if not ObjectId.is_valid(id):
        raise HTTPException(
            status_code=400,
            detail="Invalid request ID"
        )

    result = service_requests.delete_one(
        {"_id": ObjectId(id)}
    )

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Service request not found"
        )

    return {
        "message": "Service request deleted successfully"
    }









