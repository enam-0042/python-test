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

    def _check_valid(self, path:Path)->bool:
        self.texture_source_path = Path (path) / 'textures'
        if self.texture_source_path.exists() and self.texture_source_path.is_dir() :
            return True
        else :
            return False
    

    def create_texture_data(self, path:Path) -> list:

        if not self._check_valid( path=path):
            return []
        
        final_list = []

        try:
            for texture_item in self.texture_source_path.iterdir():
            # for item in os.listdir(self.texture_source_path):
                item = texture_item.name
                item_path = Path(self.texture_source_path)/ item
                last_modified_time = os.path.getmtime(item_path)
                item_name = item.split('.')
                item_data = {
                    "lastModifiedTime": last_modified_time,
                    "textureImage" : str(item),
                    "thumbUrl": f'{item_name[0]}.webp'
                }
                final_list.append(item_data)
            return final_list
        except Exception as e:
            logger.error(f'Error happened {e}')
            return []