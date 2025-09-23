import os
import json
from PIL import Image
import pandas as pd
from pathlib import Path
from core.config import settings
from store.global_store import global_store
def save_poster_json(json_data:dict, output_filename:str):

    try:
        json_filename=f'''{settings.JSON_STORE_LOCATION}/{output_filename}.json'''
        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=4)
        print(f"✅ Successfully created '{json_filename}' with {len(json_data['list'])} items.")
    except IOError as e:
        print(f"❌ Error writing to file '{json_filename}': {e}")
        print(e)

def create_category(root ) :
    # print('hello create category')
    categories = []
    for category_name in os.listdir(root):
        category_dir = Path(root)/category_name
        if not os.path.isdir(category_dir):
            pass
        categories.append(str(category_name))
    # print(categories)
    global_store.set_category_list(categories=categories)



def create_poster_json(root_path, output_filename="posters", type_directory= "posters"):
 
    if not os.path.isdir(root_path):
        print(f"❌ Error: Directory not found at '{root_path}'")
        return None

    all_items = []
    directory_type_path = Path(root_path)/(type_directory)
    # print(root_path)
    for category_name in sorted(os.listdir(directory_type_path)):
        category_path =  (directory_type_path)/ Path(category_name)
        # print(category_path)
        category_priority=-1
        # print(category_name)
        # if(output_filename=='invitations'):
        #     print(category_name)
        category_csv = Path(category_path)/f'''{category_name}.csv'''
        print(category_csv)
        if  os.path.exists(category_csv):
            # print('hererere')
            df = pd.read_csv(category_csv, header=None)
            value = df.iat[0, 0]
            category_priority= value
        category_item={
            "items": [],
            "logoTypeName": category_name,
            "priority" : int(category_priority)
        }
        if not os.path.isdir(category_path):
            continue  
        for file_name in sorted(os.listdir(category_path)):
                
            if not file_name.lower().endswith('.zip'):
                continue

            item_name = os.path.splitext(file_name)[0]

            zip_file_path= Path(category_path)/ file_name
            item_folder_path = Path(category_path)/item_name

            filename_with_extension = str(next(Path(item_folder_path).glob(f"Holder.*"), None))
  

            img_name= filename_with_extension.split('/')[-1]
            placeholder_image_path = Path(item_folder_path) / (img_name)

            
            placeholder_csv_path = Path(item_folder_path) / f'''1.csv'''
            placeholder_csv_path= Path(category_path) / placeholder_csv_path
            # if category_name=='Creativity':
            #     print(file_name)
            #     print(item_folder_path)
            # print(placeholder_csv_path)
            promo = True
            if  os.path.exists(placeholder_csv_path):
                df = pd.read_csv(placeholder_csv_path)
                value=df.columns[0]
                promo=value
                if value== "FALSE":
                    promo= False
                else:
                    promo = True 

            if os.path.isdir(item_folder_path) and os.path.isfile(placeholder_image_path) and os.path.exists(placeholder_csv_path):
                # if category_name=='Creativity':
                    # print(item_folder_path,'\n', placeholder_image_path,'\n', placeholder_csv_path)
                # Get the zip file's last modified time in milliseconds
                mod_time_ms = int(os.path.getmtime(zip_file_path) * 1000)
                image = Image.open(placeholder_image_path)
                width, height = image.size
                item_data = {
                    "placeHolder": {
                        "placeHolderUrl": f"{category_name}/{item_name}/{img_name}",
                        "placeHolderWidth": int(width/3),
                        "placeHolderHeight": int(height/3)
                    },
                    "zipFile": f"{category_name}/{file_name}",
                    "zipLastModifiedTime": mod_time_ms,
                    "itemsNo": item_name,
                    "promo": promo
                }
                category_item["items"].append(item_data)
        # if output_filename=='invitations':
        #     print(category_item)
        all_items.append(category_item)

    final_structure = {
        "list": all_items,
        "responseString":'',
    }

    # Write the final dictionary to a JSON file
    # try:
    #     json_filename=f'''{output_filename}.json'''
    #     with open(json_filename, 'w', encoding='utf-8') as f:
    #         json.dump(final_structure, f, ensure_ascii=False, indent=4)
    #     print(f"✅ Successfully created '{json_filename}' with {len(all_items)} items.")
    # except IOError as e:
    #     print(f"❌ Error writing to file '{json_filename}': {e}")


    # print(final_structure)
    # final_structure = {"hello":"fsdfs"}
    # return json.dumps(final_structure, indent=4)
    return final_structure

if __name__ == "__main__":
    pass
