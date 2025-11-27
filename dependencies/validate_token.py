import time
from typing import Annotated

from fastapi import HTTPException, Header

from services import LegacyCryptoAlgorithm

ALLOWED_DIFF = 60*60*2 # two hours
decryptor = LegacyCryptoAlgorithm()
def validate_token(token: Annotated[str, Header(alias="secret_key")]):
    try:
        # the time comes in milliseconds from date in 1970
        time_milliseconds = decryptor.decrypt(token)

        if not time_milliseconds:
            raise HTTPException(status_code=400, detail="Invalid token")

        diff = time_milliseconds - time.time() * 1000
        if not 0<diff<ALLOWED_DIFF:
            raise HTTPException(status_code=400, detail="Invalid token")

    except:
        raise HTTPException(status_code=400, detail="Invalid Token")