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
    def _find_holder_file(self, item_path:Path) -> Path | None:
        for file in item_path.iterdir():
            if file.is_file() and file.stem.lower() == 'holder':
                return file
        # pattern = re.compile(r"Holder\..+", re.IGNORECASE)
        # for file in item_path.iterdir():
        #     if file.is_file() and pattern.match(file.name):
        #         return file
        return None
    

    def _check_valid(self, path:Path, category:str) ->bool:
        # actually path and category_path has no functional value. this could be skipped
        self.category_path = Path(path) 
        self.path = Path(path)
        if self.category_path.exists() and self.category_path.is_dir():
            return True
        else:
            return False
    def _get_sub_category_item_list(self, path:Path , category:str) -> tuple[list[dict], int]:
        item_list = []
        parent_category = -1
        for item in sorted(path.iterdir()):
            try:
                # here item like /home/gambler/Documents/poster_server_data/posters/Abstract/Abstract poster 300
                item_name = item.name
               
                if item_name.lower().endswith(( '.ds_store',  '.dstore', '.zip'))  :
                    continue

                               
                if item_name.lower().endswith('.csv'):
                    if item.exists():
                        df = pd.read_csv(item, header=None)
                        parent_category= int(df.iat[0,0])
                    continue

                # this will look for image that will have Holder as name but format can be anything like .jpg ,.webp
                # holder_file_path_with_extension =str(next(Path(item).glob("Holder.*"), None))
                holder_file_path_with_extension = self._find_holder_file(item_path=item)
                holder_img_path = Path()
                holder_img_name = None  
                if holder_file_path_with_extension is not None:
                    holder_file_path_with_extension = holder_file_path_with_extension.name
                    holder_img_name = holder_file_path_with_extension
                    holder_img_path = Path(item)/holder_img_name

                # this will look for 1.csv file this will contain 'promo' and other value , we focus only in promo 
                placeholder_csv_path = Path(item ) / '1.csv'
                promo = False
                
                if placeholder_csv_path.exists():
                    df = pd.read_csv(placeholder_csv_path)
                    if df.columns[0].lower()== 'true':
                        promo= True
                    else:
                        promo = False 
                # this will look for its '.zip' file , zip file must and must have the same name as the subcategory 
                # like 'Abstract poster 300' this must have 'Abstract poster 300.zip' file otherwise zip will be null
                zip_file_path = Path(path)/ f'{item_name}.zip'
                
                if zip_file_path.exists():
                    mod_time_ms = int(zip_file_path.stat().st_mtime)
                    zip_file_name =f'{item_name}.zip'
                else : 
                    zip_file_name = None
                    mod_time_ms = None

                if not holder_img_path.is_file():
                    holder_img_name = None
                # fetch the 'Holder/holder/HOLDER.****' image info, width , height 
                if holder_img_path.is_file():
                    image = Image.open(holder_img_path)
                    width, height = image.size
                    # placeHolderUrl = posters / Abstract poster 300 / Holder.jpg  for example   
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
                    # if no holder image than returning null element
                    continue        
                item_list.append(item_data)
            except Exception as e:
                logger.error(f'while generating {category} data Error--->{e}')
        return item_list,parent_category

            
            

    def _get_sub_category_data(self, path:Path, category:str) ->list:
        if path.exists() and path.is_dir():
            pass
        else:
            return []
        category_data_list = []
        
        for sub_category in path.iterdir():
            try:
                # here subcategory like /home/gambler/Documents/poster_server_data/posters/Abstract
                
                
                # this below logic seems unnecessary , but it has great value. sometime there is 
                # .DStore type file in this folder. or some unwanted file. should have handle those explicitly
                # if category=='logos':
                #     logger.info(sub_category.name)
                if not sub_category.is_dir():
                    continue
                
                category_priority = -1
                sub_category_name = sub_category.name
                # sub_category_csv = Path(sub_category) / f'{sub_category_name}.csv'
                # if sub_category_csv.exists():
                #     df = pd.read_csv(sub_category_csv, header=None)
                #     category_priority= df.iat[0,0]
                
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
        if not self._check_valid(path, category):
            logger.warning(f'{category} directory not found')
            return []
        data = self._get_sub_category_data(path , category=category)
        return data
    
        