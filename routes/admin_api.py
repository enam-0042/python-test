from fastapi import APIRouter

# from core.logging_config import get_logger
from data.save_file import check_and_save_file


router = APIRouter(tags=["Route-dont use now"])


@router.post("/reload")
def create_json():
    """
    A Forced Creation for files endpoint for the API root.
    """
    check_and_save_file(forced_call=True)
    return True
