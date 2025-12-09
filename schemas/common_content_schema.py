from pydantic import  BaseModel

class PlaceHolderSchema(BaseModel):
    placeHolderUrl: str
    placeHolderWidth: int 
    placeHolderHeight: int 

class CommonContentSchema(BaseModel):
    placeHolder: PlaceHolderSchema
    zipFile:str
    zipLastModifiedTime: int
    itemsNo: str
    promo: bool
    



