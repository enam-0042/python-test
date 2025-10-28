import re
from store.global_store import global_store


def get_top_trending_data(category="invitations", limit=2):
    trend_data = []
    category_data = global_store.get_category_data(category)
    category_data= category_data.get("list")
    for sub_category in category_data:
        temp_dict = {}
        temp_list = []
        for item in sub_category.get("items"):
            temp_key = item.get("zipFile")
            temp_dict[temp_key] = item
            match = re.search(r"(\d+)\.zip$", temp_key)
            match = int(match.group(1))
            temp_list.append((match, temp_key))

        temp_list = sorted(temp_list , reverse = True)
        x=0 
        sorted_list = []
        sorted_list = temp_list[:limit]   
        for x in sorted_list:
            key = x[1]
            val = temp_dict.get(key)
            trend_data.append(val)
    print(len(trend_data))
    return trend_data



    