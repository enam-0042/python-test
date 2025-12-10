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
    svg_extension_list = ('.svg')
    other_extension_list = ('.jpg', '.png', '.jpeg' , '.svg' )
    thumb_extension_list = ('.webp')
    skip_files_without_zip = ('ds_store','.dstore')
    skip_files_with_zip=('ds_store','.dstore','.zip')
    image_extension_list = ('.jpg', '.png', '.jpeg', '.webp', '.svg')


    def _check_valid(self, path:Path)->bool:
        if path.exists() and path.is_dir() :
            self.bg_source_path = path
            return True
        else :
            return False
    
    def _remove_extension_icons(self, filename:str)-> str:
        return filename.split('@')[0]


    def _generate_item_data(self, bg_category:Path) :
        # print(bg_category)
        item_dict = {}
        category_image = None
        item_data =[]
        priority = -1
        parent_category = bg_category.parent.name
        if parent_category.lower() == 'icons':
            extension_list = ('.png',)
            original_image_extension_list = ('.svg',)
        else:
            extension_list = self.thumb_extension_list
            original_image_extension_list = self.other_extension_list

        category_name = bg_category.name.lower()
        # this loop is to get map thumb images , for priority of list, and for category_image
        for item in bg_category.iterdir():
            try:
                if item.name.lower().endswith(self.skip_files_with_zip):
                    continue
                        
                item_name = item.name
                # if category_name :
                #     print(parent_category)
                if item_name.lower().endswith(extension_list):
                    if parent_category == 'icons':
                        item_dict[self._remove_extension_icons(item_name.lower())] = item_name
                        continue
                    item_dict[item.stem] = item_name

                    # print(item.stem) 

                elif item.suffix.lower() in ('.csv'):
                    if  os.path.exists(item):
                        df = pd.read_csv(item, header=None)
                        value = df.iat[0, 0]
                        priority= int(value)
                        
                if category_name == item.stem.lower() and item.suffix.lower() in self.image_extension_list:
                    category_image = str(item.name)
                    continue
            except Exception as e:  
                logger.error(f'Error happened during reading bg category items: {e}')
                continue

        # this loop is to get original images and make final item data list  
        for item in bg_category.iterdir():
            try:
                if item.name.lower().endswith(self.skip_files_with_zip):
                    continue                       
                item_name = item.name
                if not item_name.lower().endswith(original_image_extension_list):
                    continue

                originalImage = None
                
                if item.suffix.lower() in (original_image_extension_list):
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
                if bg_category.name.lower().endswith(self.skip_files_with_zip):
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