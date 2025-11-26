from .other_trending_data import get_other_top_trending_data
from .icons_trending_data import get_icon_top_trending_data

def get_top_trending_data(category="", limit=2):
    if category == "icons":
        return get_icon_top_trending_data(category=category, limit=limit)
    elif category == "textures":
        return []
    else:
        return get_other_top_trending_data(category=category, limit=limit)