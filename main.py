from fastapi import FastAPI , HTTPException
import httpx
app = FastAPI()
external_api_url = "http://127.0.0.1:8001/image"
@app.get("/")
def read_root():
    try:
        with httpx.Client(timeout=500.0) as client:
            resp = client.get(external_api_url)
            if resp.status_code != 200:
                raise HTTPException(status_code=502, detail=f"external API returned {resp.status_code}")
            else:
                return resp.json()
    except httpx.RequestError:
        raise HTTPException(status_code=502, detail="failed to reach external API")

