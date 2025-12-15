from fastapi import FastAPI
from log_config import setup_logging
import logging

# Setup logging before creating the FastAPI app
setup_logging()
logger = logging.getLogger("app")

app = FastAPI()

@app.get("/")
def read_root():
    logger.info("Root endpoint was called.")
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
def read_item(item_id: int):
    logger.debug(f"Received request for item_id: {item_id}")
    if item_id > 100:
        logger.warning(f"Item ID {item_id} is unusually large.")
    return {"item_id": item_id}