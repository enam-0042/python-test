from pydantic import BaseModel
from pathlib import Path
import os
from schemas.icon import IconCategory, IconIndividual
from utils.singleton import singleton

@singleton
class IconService():
    icon_source_path:Path

    def __check_valid(self, path)->bool:
        self.icon_source_path = Path (path) / 'icons'/ 'Icons'
        # print('checkkkk')
        if self.icon_source_path.exists() and self.icon_source_path.is_dir() :
            return True
        else :
            return False
    

    def create_json(self, path):
        if not self.__check_valid(path):
            return []
        print('helloo--------------------------------------->', self.icon_source_path)
        
        final_list = []
        try:
            for category_name in os.listdir(self.icon_source_path):
                # if category_name!="Wreaths":
                #     continue
                if category_name.endswith('.zip'):
                    continue
                # category = os.path.splitext(category_name)[0]
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
                icon_list = []
                # print(type(category_zip),'   fdsfsdfsdf')
                for icon_svg in os.listdir(category_path):
                    if icon_svg.endswith('.png'):
                        continue

                    icon_without_extension= os.path.splitext(icon_svg)[0]
                    icon_png= str(icon_without_extension) + '@3x.png'
                    icon_png_path= Path (category_path)/ icon_png
                    if icon_png_path.exists():          
                        iconPNG= str(category_name+'/'+icon_png) 
                        iconSVG = str(category_name+'/'+icon_svg)
                    else :
                        iconPNG= None
                    # icon_individual =  IconIndividual( iconSVG=iconSVG,iconPNG=iconPNG)
                    icon_individual = {
                        "iconPNG":iconPNG,
                        "iconSVG":iconSVG
                    }
                    icon_list.append(icon_individual)
                # print(len(icon_list))
                icon_category_instance = {
                    "iconTypeName":icon_type_name,
                    "priority":priority,
                    "iconZIP":category_zip,
                    "lastModifiedTime":last_modified_time,
                    "icons":icon_list
                }
                # print(icon_list)
                final_list.append(icon_category_instance)
        except Exception as e:
            print(e)
            return []
        return final_list   



        
