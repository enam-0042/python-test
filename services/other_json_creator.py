from schemas.common_content_schema import PlaceHolderSchema, CommonContentSchema
import os 
from pathlib import Path
from pydantic import BaseModel
from utils.singleton import singleton
import pandas as pd
import re
from core.log_config import get_logger
from PIL import Image
logger= get_logger()

@singleton
class OtherTypeCreationService:
    path:Path
    category_path:Path

    def _find_holder_file(self, item_path:Path) -> Path | None:
        try:
            for file in item_path.iterdir():
                if file.is_file() and file.stem.lower() == 'holder':
                    if file.suffix.lower() in ('.jpg', '.png', '.jpeg', '.webp', '.svg'):
                        return file
        except Exception as e:
            logger.error(f'Error finding holder file in {item_path}: {e}')
        return None
    
    def _read_csv_promo(self, item:Path) -> bool:
        promo = True
        for file in item.iterdir():
            if file and file.is_file() and file.suffix.lower() == '.csv' and file.stem == '1':
                try:
                    df = pd.read_csv(file)
                    if df.columns[0].lower() == 'false':
                        promo = False
                except Exception as e:
                    logger.error(f'Error reading promo info from {file}: {e}')
        return promo

    def _check_valid(self, path:Path) ->bool:
        # actually path and category_path has no functional value. this could be skipped
        self.category_path = Path(path) 
        self.path = Path(path)
        if self.category_path.exists() and self.category_path.is_dir():
            return True
        else:
            return False
    def _get_sub_category_item_list(self, path:Path , category:str) -> tuple[list[dict], int]:
        item_list = []
        parent_category_priority = -1
        zip_dict = {}
        for item in path.iterdir():
            if item.suffix.lower() == '.zip':
                zip_dict[item.stem.lower()] = item

        for item in sorted(path.iterdir()):
            try:
                # here item like /home/gambler/Documents/poster_server_data/posters/Abstract/Abstract poster 300
                item_name = item.name
               
                if item_name.lower().endswith(( '.ds_store',  '.dstore', '.zip'))  :
                    continue

                try:               
                    if item_name.lower().endswith('.csv'):
                        if item.exists():
                            df = pd.read_csv(item, header=None)
                            parent_category_priority= int(df.iat[0,0])
                        continue
                except Exception as e:
                    logger.error(f'Error reading parent category from {item}: {e}')
                    continue

                # this will look for '1.csv' file this will contain 'promo' and other value , we focus only in promo 
                promo = self._read_csv_promo(item=item)

                # this will look for its '.zip' file , zip file must and must have the same name as the subcategory 
                # like 'Abstract poster 300' this must have 'Abstract poster 300.zip' file otherwise zip will be null
                zip_file_name = '' 
                zip_file_name = zip_dict.get(item_name.lower(), Path()).name 
                last_modified_time = item.stat().st_mtime
                try:
                    if zip_file_name :
                        zip_file_path = Path(path)/ zip_file_name
                        last_modified_time = int(zip_file_path.stat().st_mtime)
                    # this will look for image that will have Holder as name but format can be anything like .jpg ,.webp
                    holder_img_path = self._find_holder_file(item_path=item)
                    if holder_img_path and holder_img_path.exists() :
                        holder_img_name = holder_img_path.name
                    # fetch the 'Holder/holder/HOLDER.****' image info, width , height 
                    if holder_img_path and holder_img_path.is_file():
                        image = Image.open(holder_img_path)
                        width, height = image.size
                except Exception as e:
                    width, height = 0,0
                    holder_img_name = ''
                    zip_file_name = ''
                    logger.error(f'Error processing holder or zip for {item}: {e}')
                    # placeHolderUrl = posters / Abstract poster 300 / Holder.jpg  for example   
                    
                place_holder= PlaceHolderSchema(
                    placeHolderUrl= f'{category}/{item_name}/{holder_img_name}' if holder_img_name else '',
                    placeHolderWidth= int(width/3),
                    placeHolderHeight= int(height/3)
                )

                item_data = CommonContentSchema(
                    placeHolder= place_holder,
                    zipFile = f'{category}/{zip_file_name}' if zip_file_name else '',
                    zipLastModifiedTime= int(last_modified_time),
                    itemsNo= item_name,
                    promo= promo           
                ).model_dump()  

                item_list.append(item_data)
            except Exception as e:
                logger.error(f'while generating  {path.parent}/{category} ///{item.name}data Error--->{e}')
        return item_list,parent_category_priority

            
            

    def _get_sub_category_data(self, path:Path, category:str) ->list:
        category_data_list = []

        for sub_category in path.iterdir():
            try:
                # here subcategory like /home/gambler/Documents/poster_server_data/posters/Abstract
            
                # ignores .ds_store and non directory files
                if not sub_category.is_dir():
                    continue
                
                category_priority = -1
                sub_category_name = sub_category.name
                category_item = {
                    "logoTypeName": sub_category_name,
                }

                category_item_list, category_priority = self._get_sub_category_item_list(path=sub_category, category= sub_category_name)
                category_item["items"] = category_item_list
                category_item["priority"] = category_priority
            except Exception as e:
                category_item = {}
                logger.error(f'error in category generation {e}')
            category_data_list.append(category_item)
        category_data_list = sorted(category_data_list, key =lambda x: x.get('priority', -1))
        return category_data_list 

    def create_other_json(self, path:Path, category )->list:
        # here path is like = /home/.../poster_server_data/posters
        # category is like 'posters' , 'banners' etc
        if not self._check_valid(path=path):
            logger.warning(f'{category} directory not found')
            return []
        data = self._get_sub_category_data(path , category=category)
        return data
    
        