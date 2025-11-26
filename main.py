# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# Create the main FastAPI application instance
# from services.generate import create_poster_json
from lifespan import lifespan
from core.config import settings
# from services.save_file import check_and_save_file
from store.global_store import global_store
from routes.api import api_router
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

app.include_router(api_router)
