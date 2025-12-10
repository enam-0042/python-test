from pydantic import BaseModel  


class BackgroundItemSchema(BaseModel):
    thumbImage: str
    originalImage: str


class BackgroundSchema(BaseModel):
    categoryName: str
    categoryThumb:str
    priority: int
    lastModifiedTime: int
    items: list[BackgroundItemSchema]