from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
from bson import ObjectId
from fastapi.responses import HTMLResponse

# --------------------------------------------------
# APP
# --------------------------------------------------

app = FastAPI(title="Hospital Support Request System")


# --------------------------------------------------
# DATABASE
# --------------------------------------------------

URL = "mongodb://127.0.0.1:27017"

client = MongoClient(URL)

db = client["hospital_support_db"]

service_requests = db["service_requests"]


# --------------------------------------------------
# SCHEMA
# --------------------------------------------------

class ServiceRequest(BaseModel):
    title: str
    description: str
    department: str
    status: str
    assigned_to: str


# --------------------------------------------------
# HELPER
# --------------------------------------------------

def request_helper(doc):
    return {
        "id": str(doc["_id"]),
        "title": doc["title"],
        "description": doc["description"],
        "department": doc["department"],
        "status": doc["status"],
        "assigned_to": doc["assigned_to"]
    }


# --------------------------------------------------
# HOME PAGE
# --------------------------------------------------

@app.get("/", response_class=HTMLResponse)
def home():

    return """
    <!DOCTYPE html>

    <html>

    <head>

        <title>Hospital Support Request System</title>

        <style>

            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
                font-family: Arial, sans-serif;
            }

            body {
                background: linear-gradient(135deg, #667eea, #764ba2);
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
            }

            .container {
                width: 90%;
                max-width: 900px;
                background: white;
                border-radius: 25px;
                padding: 45px;
                text-align: center;
                box-shadow: 0 15px 40px rgba(0,0,0,0.25);
            }

            .icon {
                font-size: 65px;
                margin-bottom: 15px;
            }

            h1 {
                color: #4f46e5;
                font-size: 38px;
                margin-bottom: 12px;
            }

            .subtitle {
                color: #666;
                font-size: 18px;
                margin-bottom: 35px;
            }

            .cards {
                display: grid;
                grid-template-columns: repeat(4, 1fr);
                gap: 18px;
                margin-bottom: 35px;
            }

            .card {
                padding: 25px 15px;
                border-radius: 15px;
                color: white;
                font-weight: bold;
                transition: transform 0.2s;
            }

            .card:hover {
                transform: translateY(-5px);
            }

            .create {
                background: #10b981;
            }

            .read {
                background: #3b82f6;
            }

            .update {
                background: #f59e0b;
            }

            .delete {
                background: #ef4444;
            }

            .card-icon {
                font-size: 30px;
                margin-bottom: 10px;
            }

            .card-title {
                font-size: 18px;
            }

            .button {
                display: inline-block;
                text-decoration: none;
                background: linear-gradient(135deg, #4f46e5, #7c3aed);
                color: white;
                padding: 15px 35px;
                border-radius: 10px;
                font-size: 17px;
                font-weight: bold;
                box-shadow: 0 5px 15px rgba(79,70,229,0.3);
            }

            .button:hover {
                opacity: 0.9;
            }

            .footer {
                margin-top: 30px;
                color: #888;
                font-size: 14px;
            }

            @media (max-width: 700px) {

                .cards {
                    grid-template-columns: repeat(2, 1fr);
                }

                h1 {
                    font-size: 28px;
                }

            }

        </style>

    </head>


    <body>

        <div class="container">

            <div class="icon">🏥</div>

            <h1>Hospital Support Request System</h1>

            <p class="subtitle">
                Manage hospital service requests easily and efficiently
            </p>


            <div class="cards">

                <div class="card create">

                    <div class="card-icon">➕</div>

                    <div class="card-title">
                        Create Request
                    </div>

                </div>


                <div class="card read">

                    <div class="card-icon">🔍</div>

                    <div class="card-title">
                        View Requests
                    </div>

                </div>


                <div class="card update">

                    <div class="card-icon">✏️</div>

                    <div class="card-title">
                        Update Request
                    </div>

                </div>


                <div class="card delete">

                    <div class="card-icon">🗑️</div>

                    <div class="card-title">
                        Delete Request
                    </div>

                </div>

            </div>


            <a class="button" href="/docs">
                🚀 Open API Documentation
            </a>


            <div class="footer">

                Hospital Support Request System • FastAPI + MongoDB

            </div>

        </div>

    </body>

    </html>
    """


# --------------------------------------------------
# CREATE
# --------------------------------------------------

@app.post("/service-requests", status_code=201)
def create_request(payload: ServiceRequest):

    request_data = payload.model_dump()

    result = service_requests.insert_one(request_data)

    new_request = service_requests.find_one(
        {"_id": result.inserted_id}
    )

    return request_helper(new_request)


# --------------------------------------------------
# READ ALL
# --------------------------------------------------

@app.get("/service-requests")
def get_all_requests():

    docs = service_requests.find()

    return [request_helper(doc) for doc in docs]


# --------------------------------------------------
# READ BY ID
# --------------------------------------------------

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


# --------------------------------------------------
# UPDATE
# --------------------------------------------------

@app.put("/service-requests/{id}")
def update_request(
    id: str,
    payload: ServiceRequest
):

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


# --------------------------------------------------
# DELETE
# --------------------------------------------------

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