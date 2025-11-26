from data.generate import create_category, save_poster_json
from store.global_store import global_store

from core.config import settings
from services.icon_json_generator import IconService
from services.other_json_creator import OtherTypeCreationService
from services.texture_json_creator import TextureService
from core.log_config import get_logger
from pathlib import Path
def check_and_save_file(forced_call:bool):
    logger = get_logger()
    icon_service = IconService()
    texture_service = TextureService()
    other_json_service = OtherTypeCreationService()
    if forced_call:
        global_store.reset_all_data()
    create_category(settings.BASE_DIRECTORY)
    categories= global_store.get_category_list()

    for category in categories :
        fetched_data = global_store.get_store_data(category)
        if category=="icons":
            try:
                data= icon_service.create_icon_data(Path(settings.BASE_DIRECTORY))
                data = {"list":data}
                if fetched_data != data:
                    global_store.set_store_data(title=category, data=data)
                    save_poster_json(json_data=data,output_filename=category )

                
            except Exception as e:
                global_store.set_store_data(title=category, data = [])
                save_poster_json(json_data=[] , output_filename=category)
                logger.error(f'Error - {e}')
            continue 
        elif category == "textures":
            try:
                data_list= texture_service.create_texture_data(settings.BASE_DIRECTORY)
                BASE_TEXTURE_PATH = Path(settings.BASE_DIRECTORY)/"textures"
                BASE_TEXTURE_PATH = str(BASE_TEXTURE_PATH)
                data : dict = {}
                data['baseUrl'] = BASE_TEXTURE_PATH
                data['textureImages'] = data_list
                if fetched_data!= data:
                    global_store.set_store_data(title=category, data = data)
                    save_poster_json(json_data=data , output_filename=category)
            except Exception as e:
                global_store.set_store_data(title=category, data = [])
                save_poster_json(json_data=[] , output_filename=category)
                logger.error(f'Error - {e}')
            continue
        try:
            
            category_path= Path(settings.BASE_DIRECTORY) / category
            category_data = other_json_service.create_other_json(category_path, category)       
        
            if fetched_data !=category_data:
                global_store.set_store_data(title=category, data=category_data)
                logger.info(category)
                save_poster_json(json_data=category_data, output_filename=category)
                logger.info('new files are created')
            else:
                logger.info('not saved')
        except Exception as e:
            logger.error(f'Error happened in creating other {e}')   
             
     