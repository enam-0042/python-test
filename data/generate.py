import os
import json 
from pathlib import Path
from core.config import settings
from store.global_store import global_store

from core.log_config import get_logger

logger = get_logger()

def create_category(root):
    try:
        categories= []
        for category_name in os.listdir(root):
            category_dir = Path(root)/category_name
            if not os.path.isdir(category_dir):
                pass
            categories.append(str(category_name))
        global_store.set_category_list(categories=categories)
    except Exception as e:
        logger.error(e)


def save_poster_json(json_data:dict, output_filename:str):
    try:
        json_filename = f'''{settings.JSON_STORE_LOCATION}/{output_filename}.json'''
        with open(json_filename, 'w' , encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=4)
        logger.info(f"✅ Successfully created '{json_filename}'.")

    except IOError as e:
        logger.error(f"❌ Error writing to file '{json_filename}': {e}")


if __name__== "__main__":
    pass