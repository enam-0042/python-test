import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):

    PROJECT_NAME: str = "Industry-Grade FastAPI Project"
    API_V1_STR: str = "/api/v1"
    BASE_DIRECTORY : str
    JSON_STORE_LOCATION: str 
    OVERLOOK_MINUTES: int = 3

    class Config:
        # This tells Pydantic to look for a .env file if it exists
        env_file = ".env"
        case_sensitive = True

# Create a single instance of the settings to be used throughout the application
settings = Settings()
