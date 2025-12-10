import asyncio
from data.save_file import check_and_save_file
from core.config import settings
from pathlib import Path

async def check_and_update():

    output_directory = Path(settings.JSON_STORE_LOCATION)
    if not output_directory.exists():
        output_directory.mkdir(parents=True, exist_ok=True)

    while True:
        check_and_save_file(forced_call=False)
        await asyncio.sleep(3*60)