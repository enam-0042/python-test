from fastapi import APIRouter

from data.save_file import check_and_save_file
from services import LegacyCryptoAlgorithm

router = APIRouter(tags=["Route-dont use now"])


@router.post("/reload")
def reload_json():
    """
    A Forced Creation for files endpoint for the API root.
    """
    check_and_save_file(forced_call=True)
    return True


@router.get("/generate_test_key/{secret_key}")
def generate_test_key(secret_key: str)->str:
    if secret_key not in ("riba","mune","otnahs","otnahsorp"):
        return "wrong secret key"
    return LegacyCryptoAlgorithm().encrypt()