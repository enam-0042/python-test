import asyncio
from services.generate import create_poster_json , save_poster_json , create_category
from store.global_store import global_store, GlobalStore
from core.config import settings
from services.save_file import check_and_save_file
async def startup_function():
    while True:
        print("hello, world")  # Replace with your actual task logic
        await asyncio.sleep(3)  # 30 minutes

async def check_and_update():


    while True:
        
        check_and_save_file(forced_call=False)

        await asyncio.sleep(60)