from pydantic import BaseModel
from typing import List

class DataModelExtractorRequest(BaseModel):
    dms_list: List["DataModelExtractorRequest.DataModelExtractorItem"]
    class DataModelExtractorItem(BaseModel):
        nome: str
        endpoint_ingestao: str
        filter: str
        pageSize: int