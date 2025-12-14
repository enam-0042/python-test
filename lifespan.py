
from services.apscheduler import start_scheduler, shutdown_scheduler
import asyncio
from fastapi import FastAPI
from data.save_file import check_and_save_file
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None,check_and_save_file, False)

    start_scheduler()
    yield
    shutdown_scheduler()   

