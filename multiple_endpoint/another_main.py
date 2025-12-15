# main.py
from fastapi import FastAPI
from pydantic import BaseModel, conint
from fastapi import FastAPI, Request
import httpx
app = FastAPI()
import json
# Request body model
class ModalRequest(BaseModel):
    modal: int=1  # only 0 or 1 allowed

@app.post("/proxy")
async def handle_modal(request: ModalRequest):
    if request.modal == 0:
        return {"message": "Modal is 0"}
    elif request.modal == 1:
        return {"message": "hello from the nginx serverrrrrrrrrr"}


