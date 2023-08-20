from pydantic import BaseModel
from typing import List

class SubmitRequestModel(BaseModel):
    titulo:str
    tema_id:str
    texto:str