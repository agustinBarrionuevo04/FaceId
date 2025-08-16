"""
Face Recognition API
--------------------

This module implements a FastAPI application that provides two main endpoints
for handling user authentication with facial recognition:

    1. /procesar-vector (POST): Verifies if a given face vector exists in the
       database and retrieves the corresponding username if found.
    2. /register (POST): Registers a new user with a provided username and
       face vector.

Dependencies:
    - FastAPI: web framework for building APIs.
    - conn_db: custom database manager for handling user data.

Responses:
    All endpoints return JSON responses, with proper status codes for success
    and error handling.
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import conn_db

app = FastAPI()


@app.post("/procesar-vector")
async def proc_vector(request: Request):
    """
    Verify if a given face vector exists in the database.

    Request Body (JSON):
        {
            "vector": "<JSON string of face embedding>"
        }

    Returns:
        200 OK:
            {
                "Exist": bool,
                "Name": str | None
            }
        400 Bad Request:
            {
                "error": "Vector not received"
            }
        500 Internal Server Error:
            {
                "error": "Server error: <details>"
            }
    """
    try:
        data = await request.json()
        vector_json = data.get("vector")

        if not vector_json:
            return JSONResponse(
                content={"error": "Vector not received"}, status_code=400
            )

        val, name = conn_db.exist_user(vector_json)
        return {"Exist": val, "Name": name}

    except Exception as e:
        return JSONResponse(
            content={"error": f"Server error: {str(e)}"}, status_code=500
        )


@app.post("/register")
async def register(request: Request):
    """
    Register a new user in the database.

    Request Body (JSON):
        {
            "vector": "<JSON string of face embedding>",
            "name": "<username>"
        }

    Returns:
        200 OK:
            {
                "message": "User '<username>' registered successfully"
            }
        400 Bad Request:
            {
                "error": "Incomplete data"
            }
        500 Internal Server Error:
            {
                "error": "Server error: <details>"
            }
    """
    try:
        data = await request.json()
        vector_json = data.get("vector")
        name = data.get("name")

        if not name or not vector_json:
            return JSONResponse(
                content={"error": "Incomplete data"}, status_code=400
            )

        conn_db.new_user(name, vector_json)
        return {"message": f"User '{name}' registered successfully"}

    except Exception as e:
        return JSONResponse(
            content={"error": f"Server error: {str(e)}"}, status_code=500
        )
