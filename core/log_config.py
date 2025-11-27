# this code is from gemini as previous code is not working


import logging
from logging.handlers import RotatingFileHandler
import os

APP_LOGGER_NAME = "Fastapi_Universal_api"

logger = logging.getLogger(APP_LOGGER_NAME)
logger.setLevel(logging.DEBUG)
LOG_DIR = "log"
os.makedirs(
    LOG_DIR, exist_ok=True
)  # This will create the directory if it doesn't exist

if not logger.handlers:
    log_format = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(log_format)
    logger.addHandler(console_handler)

    log_file_path = f"{LOG_DIR}/app.log"

    file_handler = RotatingFileHandler(
        log_file_path, maxBytes=5 * 1024 * 1024, backupCount=5
    )

    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(log_format)
    logger.addHandler(file_handler)

    logger.info(
        "Global logging configuration initialized (Console: INFO+, File: DEBUG+)"
    )


def get_logger():
    return logger
