from data.generate import create_category, save_poster_json
from store.global_store import global_store
from services.bg_json_generator import BGService

from core.config import settings
from services.icon_json_generator import IconService
from services.other_json_creator import OtherTypeCreationService
from services.texture_json_creator import TextureService
from services.wallpaper_json_generator import WallpaperService
from core.log_config import get_logger
from pathlib import Path
def check_and_save_file(forced_call:bool):
    logger = get_logger()
    # icon_service = IconService()
    bg_service = BGService()

    # texture_service = TextureService()
    other_json_service = OtherTypeCreationService()
    # wallpaper_service = WallpaperService()
    if forced_call:
        global_store.reset_all_data()
    create_category(settings.BASE_DIRECTORY)
    categories= global_store.get_category_list()

    for category in categories :
        fetched_data = global_store.get_store_data(category)
        if category in ("icons", "textures", "bgs"):

            try:
                data = bg_service.create_bg_data(Path(settings.BASE_DIRECTORY)/category)
                data = {"list":data}
                if fetched_data != data:
                    global_store.set_store_data(title=category, data = data)
                    save_poster_json(json_data=data , output_filename=category)
            except Exception as e:
                global_store.set_store_data(title=category, data = [])
                save_poster_json(json_data=[] , output_filename=category)
                logger.error(f'Error - {e}')
            
        # elif category == "textures":
        #     try:
        #         # data_list , baseUrl= texture_service.create_texture_data(settings.BASE_DIRECTORY)
        #         # BASE_TEXTURE_PATH = Path(settings.BASE_DIRECTORY)/category
        #         # BASE_TEXTURE_PATH = str(BASE_TEXTURE_PATH)
        #         # data : dict = {}
        #         # data['baseUrl'] = baseUrl
        #         # data['textureImages'] = data_list
        #         data = bg_service.create_bg_data(Path(settings.BASE_DIRECTORY)/category)
        #         data = {"list":data}
        #         if fetched_data!= data:
        #             global_store.set_store_data(title=category, data = data)
        #             save_poster_json(json_data=data , output_filename=category)
        #     except Exception as e:
        #         global_store.set_store_data(title=category, data = [])
        #         save_poster_json(json_data=[] , output_filename=category)
        #         logger.error(f'Error - {e}')

        # elif category == "wallpapers":
        #     try:
        #         data = wallpaper_service.create_wallpaper_data(Path(settings.BASE_DIRECTORY)/category)
        #         data = {"list":data}
        #         if fetched_data != data:
        #             global_store.set_store_data(title=category, data=data)
        #             save_poster_json(json_data=data,output_filename=category )
        #             logger.error(f'new files are created {category}')
        #         else:
        #             logger.info('not saved')
        #     except Exception as e:
        #         global_store.set_store_data(title=category, data = [])
        #         save_poster_json(json_data=[] , output_filename=category)
        #         logger.error(f'Error - {e}')
        # elif category in ["bgs"]:
        #     try:
        #         data = bg_service.create_bg_data(Path(settings.BASE_DIRECTORY)/category)
        #         data = {"list":data}
        #         if fetched_data != data:
        #             global_store.set_store_data(title=category, data=data)
        #             save_poster_json(json_data=data,output_filename=category )
        #             logger.info(f'new files are created {category}')
        #         else:
        #             logger.info('not saved')


        #     except Exception as e:
        #         global_store.set_store_data(title=category, data = [])
        #         save_poster_json(json_data=[] , output_filename=category)
        #         logger.error(f'Error - {e}')
        else:
            try:
                
                category_path= Path(settings.BASE_DIRECTORY) / category
                category_data = other_json_service.create_other_json(category_path, category)       
                data = {"list":category_data}
                if fetched_data !=category_data:
                    global_store.set_store_data(title=category, data=category_data)
                    logger.info(category)
                    save_poster_json(json_data=category_data, output_filename=category)
                    logger.info(f'new files are created {category}')
                else:
                    logger.info('not saved')
            except Exception as e:
                global_store.set_store_data(title=category, data = [])
                save_poster_json(json_data=[] , output_filename=category)            
                logger.error(f'Error happened in creating other {e}')   
             
     