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

    }