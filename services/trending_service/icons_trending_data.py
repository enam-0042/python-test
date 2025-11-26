import re
from store.global_store import global_store
def get_icon_top_trending_data(category="icons", limit=2):
    trend_data = []
    category_data = global_store.get_category_data(category)
    category_data = category_data['list']

    for sub_category in category_data:
        temp_dict = {}
        temp_list = []
        for item in sub_category.get("icons"):
            temp_key = item.get("iconSVG")
            # name = temp_key.split("/")[-1].split(".")
            # name = ".".join(name[:-1])
            try:
                match = re.search(r"(\d+)\.svg$", temp_key)
                match = int(match.group(1))
                temp_list.append((match, temp_key))
                temp_dict[temp_key] = item
            except  Exception as e:
                print(f"Error processing key '{temp_key}': {e}")
                
        temp_list = sorted(temp_list , reverse = True)
        sorted_list = temp_list[:limit]
        for x in sorted_list:
            key = x[1]
            val = temp_dict.get(key)
            trend_data.append(val)
    return trend_data
    

        



