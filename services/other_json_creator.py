import os 
from pathlib import Path
from pydantic import BaseModel
from utils.singleton import singleton
import pandas as pd
from core.log_config import get_logger
from PIL import Image
logger= get_logger()

@singleton
class OtherTypeCreationService:
    path:Path
    category_path:Path

    default_item_data = {
        "placeHolder": {
            "placeHolderUrl": None,
            "placeHolderWidth": None,
            "placeHolderHeight": None
        },    
        "zipFile" :None,
        "zipLastModifiedTime": None,
        "itemsNo": None,
        "promo": None           
    }

    def _check_valid(self, path:Path, category:str) ->bool:
        self.category_path = Path(path) 
        self.path = Path(path)
        if self.category_path.exists() and self.category_path.is_dir():
            return True
        else:
            return False
    def _get_sub_category_item_list(self, path:Path , category:str) -> list:
        item_list = []
        for item in path.iterdir():
            try:
                item_name = item.name
                if item_name.endswith('.zip') or item_name.endswith('.csv') :
                    continue
                
                holder_file_path_with_extension =str(next(Path(item).glob("Holder.*"), None))
                holder_img_name = holder_file_path_with_extension.split('/')[-1]
                holder_img_path = Path(item)/holder_img_name
                placeholder_csv_path = Path(item ) / '1.csv'
                promo = True
                
                if placeholder_csv_path.exists():
                    df = pd.read_csv(placeholder_csv_path)
                    value=df.columns[0]
                    promo=value
                    if value== "FALSE":
                        promo= False
                    else:
                        promo = True 
                zip_file_path = Path(path)/ f'{item_name}.zip'
                if zip_file_path.exists():
                    mod_time_ms = int(zip_file_path.stat().st_mtime)
                    zip_file_name =f'{item_name}.zip'
                else : 
                    zip_file_name = None
                if not holder_img_path.is_file():
                    # logger.info(f'holder image path {holder_img_path}')
                    holder_img_name = None
                if holder_img_path.is_file():
                    image = Image.open(holder_img_path)
                    width, height = image.size
                    item_data = {
                        "placeHolder": {
                            "placeHolderUrl": f"{category}/{item_name}/{holder_img_name}",
                            "placeHolderWidth": int(width/3),
                            "placeHolderHeight": int(height/3)
                        },    
                        "zipFile" :f'{category}/{zip_file_name}',
                        "zipLastModifiedTime": mod_time_ms,
                        "itemsNo": item_name,
                        "promo": promo           
                    }
                else :
                    item_data = self.default_item_data
            except Exception as e:
                item_data = self.default_item_data
                logger.error('while generating ',e)
            item_list.append(item_data)
        return item_list

            
            

    def _get_sub_category_data(self, path:Path, category:str) ->list:
        if path.exists() and path.is_dir():
            pass
        else:
            return []
        category_data_list = []
        for sub_category in path.iterdir():
            try:
                category_priority = -1
                sub_category_name = sub_category.name
                sub_category_csv = Path(sub_category) / f'{sub_category_name}.csv'
                if sub_category_csv.exists():
                    df = pd.read_csv(sub_category_csv, header=None)
                    category_priority= df.iat[0,0]
                
                category_item = {
                    "logoTypeName": sub_category_name,
                    "priority" : int(category_priority)
                }
                if not sub_category.is_dir():
                    continue
                category_item_list = self._get_sub_category_item_list(path=sub_category, category= sub_category_name)
                category_item["items"] = category_item_list
            except Exception as e:
                category_item = {}
                logger.error(f'error in category generation {e}')
            category_data_list.append(category_item)
        return category_data_list 

    def create_other_json(self, path:Path, category )->list:
        if not self._check_valid(path, category):
            logger.warning(f'{category} directory not found')
            return []
        data = self._get_sub_category_data(path , category=category)
        return data
    
        