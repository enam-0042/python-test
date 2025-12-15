# main.py
from fastapi import FastAPI
from pydantic import BaseModel, conint
from fastapi import FastAPI, Request
import httpx
app = FastAPI()
import json
# Request body model
class ModalRequest(BaseModel):
    modal: int=0  # only 0 or 1 allowed


TARGET_SERVER = "http://127.0.0.1:8090/proxy"

@app.post("/proxy")
async def proxy(request: ModalRequest):
    # Read the incoming JSON body
    # data = await request.json()

    # Forward it to the target server
    if request.modal==1:
        async with httpx.AsyncClient() as client:
            resp = await client.post(TARGET_SERVER, json= request.dict())
            return resp.text
    
    elif request.modal ==0:
        return {"message": "Modal is 0"}
