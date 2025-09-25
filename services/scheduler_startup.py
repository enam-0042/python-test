import asyncio
# from services.generate import create_poster_json , save_poster_json , create_category
# from store.global_store import global_store, GlobalStore
# from core.config import settings
from data.save_file import check_and_save_file
# from services.save_file import check_and_save_file
async def startup_function():
    while True:
        print("hello, world")  
        await asyncio.sleep(3) 

async def check_and_update():

    while True:
        
        check_and_save_file(forced_call=False)

        await asyncio.sleep(60*3)