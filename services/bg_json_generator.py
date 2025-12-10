from PIL import Image
from pathlib import Path
import pandas as pd
import os
from utils.singleton import singleton
from core.log_config import get_logger
logger = get_logger()

@singleton
class BGService():
    bg_source_path:Path
    def _check_valid(self, path:Path)->bool:
        if path.exists() and path.is_dir() :
            self.bg_source_path = path
            return True
        else :
            return False
    
    def _generate_item_data(self, bg_category:Path) :
        # print(bg_category)
        item_dict = {}
        category_image = None
        item_data =[]
        priority = -1
        category_name = bg_category.name.lower()
        for item in bg_category.iterdir():
            try:
                if item.name.lower().endswith(('ds_store','.dstore','.zip')):
                    continue
                        
                item_name = bg_category.name
                if item_name.lower().endswith(('.webp')):
                    item_dict[item.stem.lower()] = item_name   
                if item.suffix.lower() in ('.csv'):
                    if  os.path.exists(item):
                        df = pd.read_csv(item, header=None)
                        value = df.iat[0, 0]
                        priority= int(value)
                        
                if category_name == item.stem.lower() and item.suffix.lower() in ('.jpg', '.png', '.jpeg', '.webp'):
                    category_image = str(item.name)
                    continue
            except Exception as e:  
                logger.error(f'Error happened during reading bg category items: {e}')
                continue

        for item in bg_category.iterdir():
            try:
                if item.name.lower().endswith(('ds_store','.dstore','.zip')):
                    continue                       
                item_name = item.name
                if not item_name.lower().endswith(('.jpg', '.png','.jpeg', '.webp')):
                    continue

                originalImage = None
                if item.suffix.lower() in ('.jpg', '.png', '.jpeg'):
                    originalImage = str(item.name)
                    originalImage = f'{bg_category.name}/{originalImage}'
                thumbImage = item_dict.get(item.stem.lower(), None)
                if thumbImage :
                    thumbImage = f'{bg_category.name}/{thumbImage}'
                else:
                    thumbImage = ''
                item_data.append({
                    "originalImage": originalImage,
                    "thumbImage": thumbImage
                })
            except Exception as e:  
                logger.error(f'Error happened during reading bg category items: {e}')
                continue
        return item_data, category_image, priority

  
            
        
    
    def create_bg_data(self, path:Path) -> list:
        if not self._check_valid( path=path):
            return []
        final_list = []

        for bg_category in self.bg_source_path.iterdir():
            try:
                if bg_category.name.lower().endswith(('ds_store','.dstore','.zip')):
                    continue
                category_name = bg_category.name
                
                zip_path = Path (path) / f'{category_name}.zip'
                if not zip_path.exists():
                    zip_path= ''
                    last_modified_time = bg_category.stat().st_mtime
                else:
                    last_modified_time = zip_path.stat().st_mtime
                    zip_path = str(zip_path.name)
                item_data , category_image, priority= self._generate_item_data(bg_category)
                if category_image:
                    categoty_thumb = f'{bg_category.name}/{category_image}'
                else: 
                    categoty_thumb = ''
                final_list.append({
                    "categoryName": category_name,
                    "categoryThumb": categoty_thumb,
                    "lastModifiedTime": int(last_modified_time),
                    "priority": priority,
                    "zipFile": zip_path,
                    "items": item_data
                })


            except Exception as e:
                logger.error(f'Error happened {e}')
                return []
                # final_list.append(item_data)
        return final_list