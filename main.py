from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from lifespan import lifespan
from routes.admin_api import router as admin_api_router
from routes.v1.api import router as api_router

app = FastAPI(
    title="Trending API",
    openapi_url=f"/trending/api/v1/openapi.json",
    lifespan=lifespan
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)
app.include_router(admin_api_router)
