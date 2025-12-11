from schemas.common_content_schema import CommonContentSchema, PlaceHolderSchema    
from PIL import Image
from pathlib import Path
import pandas as pd
from utils.singleton import singleton
from core.log_config import get_logger
logger = get_logger()

@singleton
class WallpaperService():
    wallpaperSourcePath:Path

    def _check_valid(self, path:Path)->bool:
        if path and path.exists() and path.is_dir() :
            self.wallpaperSourcePath = path
            return True
        else :
            return False
    
    def _check_wallpaper(self, path:Path)->tuple[Path, Path, bool]:
        holder_path = None
        bg_path= None
        promo = True
        for item in path.iterdir():
            item_name = item.name.lower()
            if item.is_file():
                if item_name.startswith('holder.'):
                    holder_path = item
                elif item_name.startswith('bg.'):
                    bg_path = item
                elif item_name.endswith('.csv'):
                    df = pd.read_csv(item, header=None)
                    promo = df.iat[0,0].lower() == 'true'
            

        return holder_path, bg_path, promo

    # add return type 

    def _get_image_dimensions(self, image_path:Path)-> tuple[int, int]:
        try:
            with Image.open(image_path) as img:
                return img.width, img.height
        except Exception as e:
            logger.error(f'Error getting image dimensions for {image_path}: {e}')
            return None, None
        
        

    def _create_content_list(self, path :Path):
        content_list = []
        priority = -1
        category_name = path.name
        zip_dict = {}
        for item in path.iterdir():
            if item.suffix.lower() == '.zip':
                zip_dict[item.stem.lower()] = item
        for item in sorted(path.iterdir()):
            try:
                
                item_name = item.name
                if item_name.lower().endswith('.csv'):
                    try:
                        df = pd.read_csv(item, header=None)
                        priority= int(df.iat[0,0])
                        continue
                    except Exception as e:
                        logger.error(f'Error reading priority from {item}: {e}')
                        continue

                if item_name.lower().endswith(('ds_store','.dstore', '.zip')):
                    continue
                zip_path = Path(zip_dict.get(item_name.lower(), Path('')))
                try:
                    if zip_path and zip_path.exists():
                        latest_modified_time = int(zip_path.stat().st_mtime)
                    else:
                        latest_modified_time = int(item.stat().st_mtime)
                except Exception as e:
                    logger.error(f'missing zip file path {zip_path}: {e}')
                    latest_modified_time = int(item.stat().st_mtime)
                zip_file = zip_path.name if zip_path and zip_path.exists() else ''
                holder_path, bg_path, promo = self._check_wallpaper(item)

                if not holder_path or not holder_path.exists():
                    continue
                holder_name = holder_path.name
                holder_width, holder_height = self._get_image_dimensions(holder_path)

                placeholder = PlaceHolderSchema(
                    placeHolderUrl= f'{category_name}/{item_name}/{holder_name}',
                    placeHolderWidth= holder_width,
                    placeHolderHeight= holder_height
                )
                item_data = CommonContentSchema(
                    placeHolder= placeholder.model_dump(),
                    zipFile= f'{category_name}/{zip_file}' if zip_file else '',
                    zipLastModifiedTime= latest_modified_time,
                    itemsNo= item_name,
                    promo= promo
                )
                content_list.append(item_data.model_dump())
            except Exception as e:
                logger.error(f'Error while generating wallpaper content for {category_name}/{item_name}: {e}')
        return content_list, priority



    def create_wallpaper_data(self,path:Path):
        if not self._check_valid( path=path):
            return []
        final_list = []

        for category in self.wallpaperSourcePath.iterdir():
            try:
                category_name = category.name
                if category_name.endswith(('.DStore' , '.dstore','.DS_Store' , '.ds_store','.zip')):
                    continue

                category_data, priority = self._create_content_list( category)
                data = {
                    "logoTypeName": category_name,
                    "priority": priority,
                    "items": category_data
                }
                final_list.append(data)

            except Exception as e:
                logger.error(f'error while generating wallpaper data for category {category_name} : {e}')
        final_list.sort(key = lambda x:x.get('priority', -1))
        return final_list