from pydantic import BaseModel


class IconIndividual(BaseModel):
    iconSVG: str | None
    iconPNG: str | None

class IconCategory(BaseModel):
    iconTypeName: str
    priority: str
    iconZIP: str | None
    lastModifiedTime: str
    icons: list[IconIndividual]

    # def __init__(self, iconTypeName, priority, iconZIP, lastModifiedTime, icons):
    #     self.iconTypeName=iconTypeName
    #     self.priority= priority
    #     self.iconZIP = iconZIP
    #     self.lastModifiedTime = lastModifiedTime
    #     self.icons= icons
    



