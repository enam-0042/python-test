from fastapi import FastAPI
from broker import broker
from tasks import heavy_computation
app = FastAPI()

@app.on_event("startup")
async def startup():
    await broker.start()

@app.post("/process")
async def trigger_processing(payload:dict):
    task  = await heavy_computation.kiq(payload)
    return {"job_id": task.task_id}

@app.get("/result/{job_id}")
async def get_result(job_id:str):
    result = await broker.result_backend.get_result(job_id)
    if result.is_ready:
        return result.return_value
    return {"status": "pending"}