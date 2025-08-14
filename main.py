# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# Create the main FastAPI application instance
from services.generate import create_poster_json
from lifespan import lifespan
from core.config import settings
from services.save_file import check_and_save_file
from store.global_store import global_store
app = FastAPI(
    title="Trending API",
    openapi_url=f"/trending/api/v1/openapi.json",
    lifespan=lifespan
)

# --- Middleware Configuration ---
# Set up CORS (Cross-Origin Resource Sharing) middleware.
# This is important for allowing web frontends to communicate with your API.
# In a production environment, you should restrict the origins.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)


@app.get("/", tags=["Root"])
def read_root():
    """
    A welcome endpoint for the API root.
    """
    return {"message": f"Welcome to Trending Api "}

@app.get("/create", tags=["Create JSON"])
def create_json():
    """
    A Forced Creation for files endpoint for the API root.
    """
    check_and_save_file(forced_call=True)
    # create_poster_json(settings.BASE_DIRECTORY, output_filename='posters' , type_directory='posters')
    # create_poster_json(settings.BASE_DIRECTORY, output_filename='logos' , type_directory='logos')
    return {"message": f"Welcome to Trending Api "}


@app.get("/api/v2/templates/{user_id}")
async def read_user(user_id: str):
    
    response = global_store.get_category_data(category_name=user_id)
    if type(response) == str:
        return "invalid request"
    
    return {user_id: response}

# @app.get("/api/v2/trending/{}")