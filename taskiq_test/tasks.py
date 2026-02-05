import asyncio
from broker import broker

@broker.task
async def heavy_computation(data:dict) ->dict:
    await asyncio.sleep(15)
    return {
        "status": "ok",
        "result": data
    }