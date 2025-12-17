from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from core.logging_config import get_logger
from services.trending_service.all_trending_data import get_top_trending_data
from store.global_store import global_store

logger = get_logger(__name__)

router = APIRouter(
    prefix="/poster_maker/api/v1", tags=["Trending API Categories API Category Data API"]
)


@router.get("/all_categories")
def get_latest_json():
    try:
        categories = global_store.get_category_list()
        print(categories)

    except Exception as e:
        logger.error(f"Error happened: {e}")
        raise HTTPException(status_code=400, detail="error in fetching category-list")

    return JSONResponse(content=categories)


@router.get("/trending/{category}")
def trending_data_process(category: str):
    response = get_top_trending_data(category=category, limit=3)
    if isinstance(response, str):
        raise HTTPException(status_code=400, detail="error in fetching trending-list")

    return {"list": response}


@router.get("/category/{category}")
def category_data_process(category: str):
    response = global_store.get_category_data(category_name=category)
    if isinstance(response, str):
        raise HTTPException(status_code=400, detail="error in fetching category-data")

    return {"list": response}
