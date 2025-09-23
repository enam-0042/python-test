import os
import json 
from PIL import Image
import pandas as pd
from pathlib import Path
from core.config import settings
from store.global_store import global_store


def create_category(root):
    categories= []
    for category_name in os.listdir(root):
        category_dir = Path(root)/category_name
        if not os.path.isdir(category_dir):
            pass
        categories.append(str(category_name))
    global_store.set_category_list(categories=categories)



def create_category_json(root,category="posters"):
    if not os.path.isdir(root):
        print(f"Error: Directory not found at '{root}'")
        return None

    category_data_list= []

    category_path = Path(root)/category

    for sub_category in os.listdir(category_path):
        sub_category_path= Path(category_path)/ sub_category
        sub_category_csv = category_path / Path(f"{sub_category}.csv")

        if os.path.exists(sub_category_csv):
            df = pd.read_csv(sub_category_csv, header=None)
            value = df.iat[0, 0]
            sub_category_priority= value  
        sub_category_item={
            "items": [],
            "logoTypeName": sub_category,
            "priority": int(sub_category_priority)
        }          
        if not os.path.isdir(sub_category_path):
            continue

        for file_name in os.listdir(sub_category_path):
            if not file_name.lower().endswith('.zip'):
                continue
            item_name = os.path.splitext(file_name)[0]
            zip_file_path = Path(sub_category_path)/ file_name
            item_folder_path = Path(sub_category_path)/item_name

            image_with_extension = str(Path(item_folder_path).glob(f"Holder.*"))