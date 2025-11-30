import logging
from typing import Annotated

from fastapi import HTTPException, Header
from data import PersistentTokenStore
from services import LegacyCryptoAlgorithm

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
ALLOWED_DIFF_IN_MS = 1000 * 60 * 30  # 30 minutes
decryptor = LegacyCryptoAlgorithm()
store = PersistentTokenStore()


def validate_token(token: Annotated[str, Header(alias="tokenHeader")]):
    if store.get(token):
        logger.info("This secret key has already been used.")
        raise HTTPException(
            status_code=400, detail="This secret key has already been used."
        )
    # the time comes in milliseconds from date in 1970
    time_milliseconds = decryptor.decrypt(token)

    if not time_milliseconds:
        raise HTTPException(status_code=401, detail="This secret key is invalid.")

    diff = decryptor.time_diff(time_milliseconds)
    if not 0 < diff < ALLOWED_DIFF_IN_MS:
        raise HTTPException(status_code=403, detail="This secret key is expired")

    store.set(token)
