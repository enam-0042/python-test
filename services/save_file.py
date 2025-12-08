from services.generate import create_category , create_poster_json, save_poster_json
from store.global_store import global_store
from core.config import settings
def check_and_save_file(forced_call:bool):
    if forced_call:
        global_store.reset_all_data()
    create_category(settings.BASE_DIRECTORY)
    categories= global_store.get_category_list()
    # print(categories)

    for category in categories :
        category_data =   create_poster_json(settings.BASE_DIRECTORY, output_filename=category , type_directory=category)

        fetched_data = global_store.get_store_data(category)
        # if not global_store.match_previous_data(title=category , data=data):
        if fetched_data !=category_data:
            global_store.set_store_data(title=category, data=category_data)
            save_poster_json(json_data=category_data, output_filename=category)

# if __name__== "__main__":
     