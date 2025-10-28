from pydantic import BaseModel
from pathlib import Path
import os
from schemas.icon import IconCategory, IconIndividual
from utils.singleton import singleton
from core.log_config import get_logger
logger = get_logger()


@singleton
class IconService():
    icon_source_path:Path

    def __check_valid(self, path:Path)->bool:
        self.icon_source_path = Path (path) / 'icons'/ 'Icons'
        if self.icon_source_path.exists() and self.icon_source_path.is_dir() :
            return True
        else :
            return False
    
    def _create_individual_icon_list(self, path:Path)->list:
        icon_list = []
        try:
            category_name = path.name
            for item in path.iterdir():
                icon_name = item.name
                if icon_name.endswith('.png'):
                    continue
                icon_svg = icon_name
                icon_without_extension= os.path.splitext(icon_svg)[0]
                icon_png= str(icon_without_extension) + '@3x.png'
                icon_png_path= Path (path) / icon_png
            
                if icon_png_path.is_file():          
                    iconPNG= str(category_name+'/' + icon_png) 
                    iconSVG = str(category_name+'/' + icon_svg)
                else :
                    iconPNG= None
                    iconSVG= str(category_name+'/' + icon_svg)
                icon_individual = {
                    "iconPNG":iconPNG,
                    "iconSVG":iconSVG
                }
                icon_list.append(icon_individual)
        except Exception as e:
            logger.exception('error creating individual list' ,e)
        return icon_list

    def create_icon_data(self, path:Path):
        if not self.__check_valid(path):
            return []        
        final_list = []
        try:
            for category in self.icon_source_path.iterdir():
                category_name = category.name
                if category_name.endswith('.zip'):
                    continue
                category_path = Path(self.icon_source_path)/ category_name
                category_zip = str(category_path)+ '.zip'
                category_zip = Path(category_zip)
                if not category_zip.exists():
                    category_zip = None
                else:
                    category_zip= category_name+'.zip'
                last_modified_time = os.path.getmtime(category_path)
                icon_type_name = category_name
                priority = None
                icon_list = self._create_individual_icon_list(category_path)
 
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
            return []
        return final_list   



        
