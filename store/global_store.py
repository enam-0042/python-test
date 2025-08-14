from typing import Any, Dict, Optional, List

class GlobalStore:
    _solo_instance = None
    # def __init__(self):
    #     pass
        # self._store: Dict[str, Dict] = {
        #     "posters" : None, 
        #     "logos" : None
        # }

    def __new__(cls):
        if cls._solo_instance is None:
            cls._solo_instance = super(GlobalStore, cls).__new__(cls)
            cls._solo_instance._store: Dict[str, Dict] = {
                "posters": None,
                "logos": None
            }
            cls._solo_instance._category_list : List = []
        return cls._solo_instance
    
    def reset_all_data(self):
        self._store={}
        self._category_list=[]


    def get_store_data(self, title:str) -> Optional[Any]:
        # print(self._store)
        # return self._store[title]
        return self._store.get(title)
    def set_store_data(self, title:str, data:Any) :
        self._store[title] = data
    def match_previous_data(self, title:str, data:Any) ->bool:
        print('here is mactching' , self._store[title])
        return self._store.get(title) == data
  
    def get_category_list(self) -> List:
        return self._category_list
    
    def set_category_list(self , categories:List):
        self._category_list= categories
        # print(self._category_list)

    def get_category_data(self, category_name:str) -> Any:
        if category_name not in self._category_list:
            return "no category found"
        category_data= self._store[category_name]
        return category_data



global_store = GlobalStore()