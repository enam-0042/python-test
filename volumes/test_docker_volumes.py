import shutil
from pathlib import Path
import secrets
import string
from fastapi import FastAPI

app = FastAPI()

# Configuration
STAGING_DIR = Path("/home/gambler/random")
FINAL_DIR = Path("/tmp/.temp/random")


@app.post("/create-and-move")
async def create_and_move_file():
    # 1. Ensure both directories exist
    STAGING_DIR.mkdir(parents=True, exist_ok=True)
    FINAL_DIR.mkdir(parents=True, exist_ok=True)

    # 2. Generate a random filename
    random_str = "".join(
        secrets.choice(string.ascii_letters + string.digits) for _ in range(10)
    )
    filename = f"{random_str}.txt"

    staging_path = STAGING_DIR / filename
    final_path = FINAL_DIR / filename

    # 3. Write 'hello world' to the staging file
    with open(staging_path, "w") as f:
        f.write("hello world")

    # 4. Move the file from staging to final destination
    # shutil.move is safer than os.rename for Docker volume boundaries
    shutil.move(str(staging_path), str(final_path))

    return {
        "status": "file moved successfully",
        "original_loc": str(staging_path),
        "final_loc": str(final_path),
        "filename": filename,
        "content": Path.cwd(),
    }
