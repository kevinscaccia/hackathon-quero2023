from pydantic import BaseModel
from typing import List
class EssayModel(BaseModel):
    texto_redacao: str
    titulo: str
    theme_id: str
    nota_final: int
    crit_1_nota: int
    crit_2_nota: int
    crit_3_nota: int
    crit_4_nota: int
    crit_5_nota: int
    comentarios: str