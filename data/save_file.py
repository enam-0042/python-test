from data.generate import create_category , create_category_json, save_poster_json
from store.global_store import global_store
from core.config import settings
from services.icon_json_generator import IconService

def check_and_save_file(forced_call:bool):
    icon_service = IconService()

    if forced_call:
        global_store.reset_all_data()
    create_category(settings.BASE_DIRECTORY)
    categories= global_store.get_category_list()
    print(categories)

    for category in categories :
        if category=="icons":
            data= icon_service.create_json(settings.BASE_DIRECTORY)
            # print(data)
            data = {"list":data}
            save_poster_json(json_data=data,output_filename=category )
            print('here')
            continue
        category_data =   create_category_json(settings.BASE_DIRECTORY, category=category )
        fetched_data = global_store.get_store_data(category)
        if fetched_data !=category_data:
            global_store.set_store_data(title=category, data=category_data)
            save_poster_json(json_data=category_data, output_filename=category)
            print('new files are created')
        
        else:
            print('not saved')

# if __name__== "__main__":
     