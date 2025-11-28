import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from services.scheduler_startup import check_and_update

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app:FastAPI):
    task = asyncio.create_task(check_and_update())
    logger.info("Check and update task started")

    yield

    task.cancel()
    logger.info("Check and update gracefully stopped")

    await task

