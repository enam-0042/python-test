

from fastapi import APIRouter
from store.global_store import global_store
router = APIRouter(*, prefix="/api/v1/")

@router.get("/latest-json")
def get_latest_json():
    
    # if store["generated_json"] is None:
    #     return {"status": "pending", "message": "No data generated yet"}
    # return {
    #     "status": "success",
    #     "last_updated": store["last_updated"],
    #     "data": store["generated_json"]
    # }