from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Hospital Support Request System"}


# Database
db = {
    1: {
        "id": 1,
        "patient_name": "Ravi",
        "room_no": 101,
        "request_type": "Medicine",
        "description": "Need prescribed medicine",
        "status": "NEW"
    },
    2: {
        "id": 2,
        "patient_name": "Anitha",
        "room_no": 202,
        "request_type": "Nurse",
        "description": "Need nurse assistance",
        "status": "NEW"
    }
}


# Schemas
class ServiceRequestCreate(BaseModel):
    patient_name: str
    room_no: int
    request_type: str
    description: str
    status: str


class ServiceRequestResponse(ServiceRequestCreate):
    id: int


# GET - Get all requests
@app.get("/service-requests")
def service_request_read_all():
    return list(db.values())


# GET - Get request by ID
@app.get("/service-requests/{id}")
def service_request_read_by_id(id: int):
    if id not in db:
        raise HTTPException(
            detail="Service request not found",
            status_code=404
        )

    return db[id]


# POST - Create request
@app.post(
    "/service-requests",
    status_code=201,
    response_model=ServiceRequestResponse
)
def service_request_create(request_payload: ServiceRequestCreate):

    new_id = max(db.keys(), default=0) + 1

    db[new_id] = {
        "id": new_id,
        **request_payload.model_dump()
    }

    return db[new_id]


# PUT - Update request
@app.put(
    "/service-requests/{id}",
    response_model=ServiceRequestResponse
)
def service_request_update(
    id: int,
    payload: ServiceRequestCreate
):

    if id not in db:
        raise HTTPException(
            detail="Service request not found",
            status_code=404
        )

    db[id] = {
        "id": id,
        **payload.model_dump()
    }

    return db[id]


# DELETE - Delete request
@app.delete("/service-requests/{id}")
def service_request_delete(id: int):

    if id not in db:
        raise HTTPException(
            detail="Service request not found",
            status_code=404
        )

    del db[id]

    return {
        "message": "Service request deleted successfully"
    }