import logging
from typing import Annotated

from fastapi import HTTPException, Header

from services import LegacyCryptoAlgorithm

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
ALLOWED_DIFF_IN_MS = 1000*60*60*2 # two hours
decryptor = LegacyCryptoAlgorithm()

def validate_token(token: Annotated[str, Header(alias="secret_key")]):
    try:
        # the time comes in milliseconds from date in 1970
        time_milliseconds = decryptor.decrypt(token)
        logger.info(f"Time: {time_milliseconds=}, {decryptor.time_diff(time_milliseconds)=}")
        if not time_milliseconds:
            raise HTTPException(status_code=400, detail="Invalid token or expired")

        diff = decryptor.time_diff(time_milliseconds)
        if not 0<diff<ALLOWED_DIFF_IN_MS:
            raise HTTPException(status_code=400, detail="Invalid token or expired")

    except:
        raise HTTPException(status_code=400, detail="Invalid token or expired")