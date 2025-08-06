from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import json
import numpy as np
from face_auth import conn_db

app = FastAPI()


@app.post("/procesar-vector")
async def proc_vector(request: Request):
    try:
        data = await request.json()
        vector_json = data.get("vector")
        if not vector_json:
            return JSONResponse(content={"error": "Vector no recibido"}, status_code=400)

        val, name = conn_db.exist_user(vector_json)
        return {"Exist": val, "Name": name}
    except Exception as e:
        return JSONResponse(content={"error": f"Server error: {str(e)}"}, status_code=500)


@app.post("/register")
async def register(request: Request):
    try:
        data = await request.json()
        vector_json = data.get("vector")
        name = data.get("name")
        if not name or not vector_json:
            return JSONResponse(content={"error": "Datos incompletos"}, status_code=400)

        conn_db.new_user(name, vector_json)
        return {"message": f"Usuario '{name}' registrado correctamente"}
    except Exception as e:
        return JSONResponse(content={"error": f"Server error: {str(e)}"}, status_code=500)
