from fastapi import FastAPI
from broker import broker
from tasks import heavy_computation
import asyncio
app = FastAPI()

# @app.on_event("startup")
# async def startup():
#     await broker.start()



@app.post("/process")
async def trigger_processing(payload:dict):
    task  = await heavy_computation.kiq(payload)
    return {"job_id": task.task_id}

# @app.get("/result/{job_id}")
# async def get_result(job_id:str):
#     # try:
#     result = await broker.result_backend.get_result(job_id)
#     if result.is_result_ready():
#         return result.return_value
#     # except Exception as e:
#     #     return {"status": "error", "message": str(e)}
#     return {"status": "pending"}

@app.get("/result/{job_id}")
async def get_result(job_id:str):
    try:
        result = await broker.result_backend.get_result(job_id)
        return {
            "status": "calculation done",
            "result": result.return_value,
            "execution_time": result.execution_time
        }
    except ResultIsMissingError:
        return {"status": "pending"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 

# async def run_example():
#     task = await heavy_computation.kiq({"key": "val,m,m,m,m,m,ue"})
#     print(task)
#     print(f'task sent, task id: {task.task_id}')

#     result = await task.wait_result(timeout=100) 
#     print(f"Result: {result} \n {result.return_value} ")
#     await broker.shutdown()
    # if not result.is_err:
    #     print(f"Success: {result.return_value}")
    # else:
    #     print(f"Error: {result.exception}") 

# if __name__ == "__main__":
#     asyncio.run(run_example())