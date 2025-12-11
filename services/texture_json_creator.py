# waiting to be removed
import os
from pathlib import Path
from pydantic import BaseModel 
from utils.singleton import singleton
# from core.logging_config import get_logger
from core.log_config import get_logger

logger = get_logger()


@singleton
class TextureService:
    texture_source_path:Path
    texture_specific_path:Path = Path('textures')

    def _check_valid(self, path:Path)->bool:
        self.texture_source_path = Path (path) / self.texture_specific_path
        if self.texture_source_path.exists() and self.texture_source_path.is_dir() :
            return True
        else :
            return False
    
    def _item_dict_creation(self, item_path:Path) -> dict:
        try:
            item_name = item_path.name
            last_modified_time = os.path.getmtime(item_path)
            fmt = 'webp'
            item_data = {
                "lastModifiedTime": last_modified_time,
                "textureImage" : str(item_name),
                "thumbUrl": f'{item_name.split(".")[0]}.{fmt}'
            }
        except Exception as e:
            logger.error(f'Error happened during item dict creation: {e}')
            item_data = {}  
        return item_data      
    def _texture_list_creation(self, path:Path) -> list[dict]:
        texture_dict = {}
        for texture_item in path.iterdir():
            
            if texture_item.name.lower().endswith(('ds_store','.dstore')):
                continue


    def create_texture_data(self, path:Path) -> list:
        if not self._check_valid( path=path):
            return []
        final_list = []
        try:
            item_list = self._texture_list_creation(self.texture_source_path)
        except Exception as e:
            logger.error(f'Error happened during texture list creation: {e}')
            item_list = []
        final_list.extend(item_list)
        return final_list , str(self.texture_source_path)


        # try:
        #     for texture_item in self.texture_source_path.iterdir():
        #         if texture_item.name.lower().endswith(('ds_store','.dstore')):
        #             continue
                
        #         item_data  = self._item_dict_creation(item_path=texture_item)
        #         final_list.append(item_data)
        #     return final_list , str(self.texture_source_path)
        # except Exception as e:
        #     logger.error(f'Error happened {e}')
        #     return []