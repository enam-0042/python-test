import asyncio
import base64
import os
from pathlib import Path
from typing import List, Dict, Any

import httpx
from pydantic import BaseModel, HttpUrl


class ImageRequest(BaseModel):
    image: str
    upscale: bool
    name: str


class AppConfig:
    SOURCE_DIR = Path("/home/gambler/Documents/scratchtest/1024")
    REMOTE_URL = "http://47.155.229.45:40868/ai/api/v1/scratch_remove"
    ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg"}


async def process_image(client: httpx.AsyncClient, file_path: Path) -> Dict[str, Any]:
    try:
        with open(file_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode("utf-8")

        payload = ImageRequest(image=encoded_string, upscale=True, name=file_path.name)
        response = await client.post(AppConfig.REMOTE_URL, json=payload.model_dump())
        response.raise_for_status()
        return {"status": "success", "file": file_path.name, "data": response.json()}
    except Exception as e:
        return {"status": "error", "file": file_path.name, "error": str(e)}


async def main():
    results = []
    files = [
        f
        for f in AppConfig.SOURCE_DIR.iterdir()
        if f.suffix.lower() in AppConfig.ALLOWED_EXTENSIONS
    ]

    async with httpx.AsyncClient(timeout=900) as client:
        tasks = [process_image(client, file) for file in files]
        results = await asyncio.gather(*tasks)

    for result in results:
        print("Processed:", result)

    return results


if __name__ == "__main__":
    AppConfig.SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    response = asyncio.run(main())
