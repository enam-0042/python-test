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

    def __check_valid(self, path)->bool:
        self.texture_source_path = Path (path) / 'textures'
        # logger.info("uuuuuuu")
        if self.texture_source_path.exists() and self.texture_source_path.is_dir() :
            return True
        else :
            return False
    
    def create_texture_data(self, path) -> list:
        # print('hello this is new world')
        # logger.info("self.__check_valid(self, path=path)")
        # self.__check_valid(path=path)
        if not self.__check_valid( path=path):
            return []
        
        final_list = []

        try:
            for item in os.listdir(self.texture_source_path):
                item_path = Path(self.texture_source_path)/ item
                last_modified_time = os.path.getmtime(item_path)
                item_data = {
                    "lastModifiedTime": last_modified_time,
                    "textureImage" : str(item)
                }
                final_list.append(item_data)
                # logger.info(f"file name- {texture}")
            return final_list
        except Exception as e:
            logger.error(f'Error happened {e}')
            return []