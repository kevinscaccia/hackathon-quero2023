from pydantic import BaseModel
from typing import List

class ThemeModelResponse(BaseModel):
    themeList: List["ThemeModelResponse.ThemeModelItem"]
    class ThemeModelItem(BaseModel):
        id:int
        titulo:str
        texto_base:str
