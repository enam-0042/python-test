from pydantic import BaseModel
from pathlib import Path
import os
import pandas as pd
from schemas.icon import IconCategory, IconIndividual
from utils.singleton import singleton
from core.log_config import get_logger
logger = get_logger()


@singleton
class IconService():
    icon_source_path:Path
    icon_specific_path:Path = Path('icons') 

    def __check_valid(self, path:Path)->bool:
        self.icon_source_path = Path (path) / self.icon_specific_path
        if self.icon_source_path.exists() and self.icon_source_path.is_dir() :
            return True
        else :
            return False


    def _create_individual_icon_list(self, path:Path)-> tuple[list[dict], int]:
        icon_list = []
        category_name = path.name
        # currently no priority for individual icons is defined in csv or anywhere, so setting it to None
        # if future requirement arises, we can modify it accordingly
        priority = -1
        for item in sorted(path.iterdir()):
            try:
                if item.name.endswith('.csv'):
                    if item.exists():
                        df = pd.read_csv(item, header = None)
                        priority= int(df.iat[0,0])
                icon_name = item.name
                if icon_name.endswith('.png'):
                    continue
                icon_svg = icon_name
                icon_without_extension= os.path.splitext(icon_svg)[0]
                icon_png= str(icon_without_extension) + '@3x.png'
                icon_png_path= Path (path) / icon_png
            
                iconSVG = str(category_name+'/' + icon_svg)
                if icon_png_path.is_file():          
                    iconPNG= str(category_name+'/' + icon_png) 
                else :
                    iconPNG= None
                icon_individual = {
                    "iconThumb":iconPNG,
                    "iconOriginal":iconSVG
                }
                icon_list.append(icon_individual)
            except Exception as e:
                logger.exception('error creating individual list' ,e)
        # icons = {
        #     "priority":priority,
        #     "icons":icon_list
        # }
        return icon_list, priority
        # return icons

    def create_icon_data(self, path:Path):
        if not self.__check_valid(path):
            return []        
        final_list = []
        print(self.icon_source_path)
        for category in self.icon_source_path.iterdir():
            try:
                category_name = category.name
                if category_name.endswith('.zip'):
                    continue
                if category_name.endswith(('.DStore' , '.dstore')):
                    continue
                
                if category_name.endswith(('.DS_Store' , '.ds_store')):
                    continue                
                # category_path = Path(self.icon_source_path)/ category_name
                # category_zip = str(category_path)+ '.zip'
                category_zip = Path(self.icon_source_path)/ (category_name + '.zip')
                if not category_zip.exists():
                    # logger.warning(f'zip file not found for category {category_zip}')
                    category_zip = None
                else:
                    category_zip= category_name+'.zip'
                last_modified_time = os.path.getmtime(category)
                icon_type_name = category_name
                priority = None
                icon_list , priority = self._create_individual_icon_list(category)
 
                icon_category_instance = {
                    "iconTypeName":icon_type_name,
                    "priority":priority,
                    "iconZIP":category_zip,
                    "lastModifiedTime":last_modified_time,
                    "icons":icon_list
                }
                final_list.append(icon_category_instance)
            except Exception as e:
                logger.error(f'Error - {e}')
        # return []
        return sorted(final_list , key= lambda x: x.get('priority', -1))
    
        # return final_list   



        
