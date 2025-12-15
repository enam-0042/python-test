# ...existing code...
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import os
import base64
import mimetypes
import asyncio
app = FastAPI()

IMAGE_DEFAULT = "image.jpeg"  # file must be in the same directory

@app.get("/")
async def read_root():
    return {"message": "Hello, world!"}

@app.get("/image")
async def serve_image(filename: str = IMAGE_DEFAULT):
    if not os.path.isfile(filename):
        raise HTTPException(status_code=404, detail="image not found")
    await asyncio.sleep(125)  # simulate async operation
    try:
        ctype, _ = mimetypes.guess_type(filename)
        ctype = ctype or "application/octet-stream"
        with open(filename, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("ascii")
        # return filename, content type and raw base64 string
        return JSONResponse({"filename": filename, "content_type": ctype, "data": b64})
    except Exception:
        raise HTTPException(status_code=500, detail="failed to read image")
# ...existing code...