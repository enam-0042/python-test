from data.generate import create_category , create_category_json, save_poster_json
from store.global_store import global_store
from core.config import settings
from services.icon_json_generator import IconService
from services.texture_json_creator import TextureService
from core.log_config import get_logger
from pathlib import Path
def check_and_save_file(forced_call:bool):
    logger = get_logger()
    icon_service = IconService()
    texture_service = TextureService()
    if forced_call:
        global_store.reset_all_data()
    create_category(settings.BASE_DIRECTORY)
    categories= global_store.get_category_list()

    for category in categories :
        fetched_data = global_store.get_store_data(category)
        if category=="icons":
            try:
                data= icon_service.create_icon_data(Path(settings.BASE_DIRECTORY))
                # print(data)
                data = {"list":data}
                if fetched_data != data:
                    global_store.set_store_data(title=category, data=data)
                    save_poster_json(json_data=data,output_filename=category )
                # print('here')
                
            except Exception as e:
                logger.error(f'Error - {e}')
            continue 
        if category == "textures":
            try:
                data_list= texture_service.create_texture_data(settings.BASE_DIRECTORY)
                BASE_TEXTURE_PATH = Path(settings.BASE_DIRECTORY)/"textures"
                BASE_TEXTURE_PATH = str(BASE_TEXTURE_PATH)
                # logger.info(type(data))
                data = {}
                data['baseUrl'] = BASE_TEXTURE_PATH
                data['textureImages'] = data_list
                if fetched_data!= data:
                    global_store.set_store_data(title=category, data = data)
                    save_poster_json(json_data=data , output_filename=category)
            except Exception as e:
                logger.error(f'Error - {e}')
            continue

        category_data =   create_category_json(settings.BASE_DIRECTORY, category=category )    
        
       
        if fetched_data !=category_data:
            global_store.set_store_data(title=category, data=category_data)
            logger.info(category)
            save_poster_json(json_data=category_data, output_filename=category)
            logger.info('new files are created')
        
        else:
            logger.info('not saved')

# if __name__== "__main__":
     