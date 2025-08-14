import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from services.scheduler_startup import startup_function , check_and_update


@asynccontextmanager
async def lifespan(app:FastAPI):
    task = asyncio.create_task(check_and_update())
    print('BG function started')

    yield

    task.cancel()

    try:
        await task
    
    except asyncio.CancelledError:
        print("Background Task stopped.")
    
    print("Shutdown occured")






# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     # Startup
#     task = asyncio.create_task(startup_function())
#     print("🚀 Background task started.")

#     yield  # Application runs

#     # Shutdown
#     task.cancel()
#     try:
#         await task
#     except asyncio.CancelledError:
#         print("🛑 Background task stopped.")
#     print("✅ Application shutdown complete.")
