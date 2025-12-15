import logging.config
import json

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        },
        "json": {
            "class": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "format": "%(asctime)s %(levelname)s %(name)s %(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
            "level": "INFO"
        },
        "file_handler": {
            "class": "logging.FileHandler",
            "formatter": "standard",
            "filename": "app.log"
        },
        "json_file_handler": {
            "class": "logging.FileHandler",
            "formatter": "json",
            "filename": "app_json.log"
        }
    },
    "loggers": {
        "uvicorn": {
            "handlers": ["console"],
            "level": "INFO"
        },
        "app": {
            "handlers": ["console", "file_handler"],
            "level": "DEBUG",
            "propagate": False
        },
        "request_logger": {
            "handlers": ["json_file_handler"],
            "level": "INFO",
            "propagate": False
        }
    }
}

def setup_logging():
    logging.config.dictConfig(LOGGING_CONFIG)