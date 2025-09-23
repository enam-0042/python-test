from fastapi import APIRouter
from routes.root import router as root_router 
from routes.v1.creation import router as v1_creation_router
# from routes.v2.templates import router as v2_templates_router

api_router = APIRouter()

api_router.include_router(root_router)
api_router.include_router(v1_creation_router)
