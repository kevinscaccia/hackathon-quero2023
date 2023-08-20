from pydantic import BaseModel
from typing import List

class SubmitModelExtractorRequest(BaseModel):
    id_analise:int
    nota_final:int
    nota_criterios: List["NotaCriteriosItem"]
    class NotaCriteriosItem(BaseModel):
        criterio:int
        nota:int
    comentarios:List[str]
