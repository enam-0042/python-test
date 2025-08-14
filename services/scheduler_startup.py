import asyncio
from services.generate import create_poster_json , save_poster_json , create_category
from store.global_store import global_store, GlobalStore
from core.config import settings
from services.save_file import check_and_save_file
async def startup_function():
    while True:
        print("hello, world")  # Replace with your actual task logic
        await asyncio.sleep(3)  # 30 minutes

async def check_and_update():


    while True:
        
        check_and_save_file(forced_call=False)
        # print('lfsjlfsjlfsjk')
        
        # news=  GlobalStore()
        # print( global_store is news)
        # create_category(settings.BASE_DIRECTORY)
        # categories= global_store.get_category_list()
        # for category in categories :
        #     data =   create_poster_json(settings.BASE_DIRECTORY, output_filename=category , type_directory=category)
        #     if not global_store.match_previous_data(title=category , data=data):
        #         global_store.set_store_data(title=category, data=data)
        #         save_poster_json(json_data=data, output_filename=category)
        #         print('new files are created')
        #     else:
        #         print('not saved')

        # data =   create_poster_json(settings.BASE_DIRECTORY, output_filename='posters' , type_directory='posters')

        # if not global_store.match_previous_data(title='posters', data=data) :
        #     print('saved')
        #     global_store.set_store_data(title='posters' , data=data)
        #     save_poster_json(json_data=data , output_filename='posters')
        # else : 
        #     print('not saved')
        await asyncio.sleep(60)