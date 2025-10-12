import os
import json 
from PIL import Image
import pandas as pd
from pathlib import Path
from core.config import settings
from store.global_store import global_store
from services import icon_json_generator

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
    for sub_category in sorted(os.listdir(category_path)):
        sub_category_path= Path(category_path)/ sub_category
        sub_category_csv = sub_category_path / Path(f"{sub_category}.csv")
        sub_category_priority=-1
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

            image_path_with_extension = str(next(Path(item_folder_path).glob(f"Holder.*"),None))
            image_name= image_path_with_extension.split('/')[-1]
            image_path  = Path(item_folder_path)/ image_name
            item_csv_path= Path(item_folder_path)/ "1.csv"
            promo = True

            if os.path.exists(item_csv_path):
                # print(item_csv_path)
                df = pd.read_csv(item_csv_path)
                value=df.columns[0]
                promo=value
                if value== "FALSE":
                    promo= False
                else:
                    promo = True 
            
            
            if os.path.isdir(item_folder_path) and os.path.isfile(image_path) and os.path.exists(item_csv_path):
                mod_time_ms = int(os.path.getmtime(zip_file_path)*1000)
                image = Image.open(image_path)
                width, height = image.size
                image_data = {
                    "placeHolder": {
                        "placeHolderUrl": f"{sub_category}/{item_name}/{image_name}",
                        "placeHolderWidth": int(width/3),
                        "placeHolderHeight": int(height/3)
                    },
                    "zipFile": f"{sub_category}/{file_name}",
                    "zipLastModifiedTime": mod_time_ms,
                    "itemsNo": item_name,
                    "promo": promo                    
                }

                sub_category_item["items"].append(image_data)
        category_data_list.append(sub_category_item)           
    final_structure = {
        "list": category_data_list,
        "responseString":'',
    }  

    return final_structure 


def save_poster_json(json_data:dict, output_filename:str):
    try:
        json_filename = f'''{settings.JSON_STORE_LOCATION}/{output_filename}.json'''
        with open(json_filename, 'w' , encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=4)
        print(f"✅ Successfully created '{json_filename}' with {len(json_data['list'])} items.")

    except IOError as e:
        print(f"❌ Error writing to file '{json_filename}': {e}")


if __name__== "__main__":
    pass