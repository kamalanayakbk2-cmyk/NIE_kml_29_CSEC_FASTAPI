from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI()


@app.get("/")
def home():
    return {"message": "Enterprise IT Service Desk"}


db = {
    1: {
        "id": 1,
        "title": "Computer is not on",
        "description": "Power button is not working",
        "category": "Hardware",
        "status": "NEW",
    },
    2: {
        "id": 2,
        "title": "Internet is not working",
        "description": "WiFi problem",
        "category": "Network",
        "status": "NEW",
    },
}


class TicketCreate(BaseModel):
    title: str
    description: str
    category: str
    status: str


class TicketResponse(TicketCreate):
    id: int


@app.get("/tickets")
def ticket_read_all():
    return list(db.values())


@app.get("/tickets/{id}")
def ticket_read_by_id(id: int):
    if id not in db:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found",
        )

    return db[id]


@app.post(
    "/tickets",
    status_code=201,
    response_model=TicketResponse,
)
def ticket_create(ticket_payload: TicketCreate):
    new_id = max(db.keys(), default=0) + 1

    db[new_id] = {
        "id": new_id,
        **ticket_payload.model_dump(),
    }

    return db[new_id]


@app.put(
    "/tickets/{id}",
    response_model=TicketResponse,
)
def ticket_update(id: int, payload: TicketCreate):
    if id not in db:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found",
        )

    db[id] = {
        "id": id,
        **payload.model_dump(),
    }

    return db[id]


@app.delete("/tickets/{id}")
def ticket_delete(id: int):
    if id not in db:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found",
        )

    del db[id]

    return {
        "message": "Ticket deleted successfully",
    }