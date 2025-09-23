from fastapi import APIRouter, HTTPException
from typing import Dict , Any
from core.logging_config import get_logger
from store.global_store import global_store
from schemas.creation import ApiResponse, ErrorResponse
from fastapi.responses import JSONResponse
logger = get_logger(__name__)

router = APIRouter(prefix='/api/v1', tags=["v1/creation-bro"])
@router.get("/latest-json")
def get_latest_json():
    try:
        categories = global_store.get_category_list()
        print(categories)

    
    except Exception as e:
        logger.error(f"Error happened: {e}")
        raise HTTPException(status_code=400, detail="error in fetching category-list")

    return JSONResponse(content=categories)


