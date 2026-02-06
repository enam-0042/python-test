import asyncio
from broker import broker

async def calculate(upper:int)->int:
    sum =1
    for i in range(upper):
        sum= sum+i
    return sum
@broker.task
async def heavy_computation(data:dict) ->int:
    datas = await calculate(900000000)
    return {
        "status": "ok",
        "result": datas
    }

@broker.task
async def send_notification(email:str, message:str) -> None:
    # await asyncio.sleep(1)
    print(f"Notification sent: {message}")