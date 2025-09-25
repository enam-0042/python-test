from fastapi import APIRouter
# from core.logging_config import get_logger
from data.save_file import check_and_save_file


router = APIRouter(tags=["U just Landed"])

@router.get("/create", tags=["Create JSON"])
def create_json():
    """
    A Forced Creation for files endpoint for the API root.
    """
    check_and_save_file(forced_call=True)
    # create_poster_json(settings.BASE_DIRECTORY, output_filename='posters' , type_directory='posters')
    # create_poster_json(settings.BASE_DIRECTORY, output_filename='logos' , type_directory='logos')
    return {"message": "Welcome to Trending Api"}
