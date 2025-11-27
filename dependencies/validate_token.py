from typing import Annotated

from fastapi import HTTPException, Header

from services import DecryptToken

ALLOWED_DIFF = 60*60*2 # two hours
decryptor = DecryptToken()
def validate_token(token: Annotated[str, Header()]):
    try:
        secret = decryptor.decrypt(token)
        if not secret:
            raise HTTPException(status_code=400, detail="Invalid token")
    except:
        raise HTTPException(status_code=400, detail="Invalid Token")