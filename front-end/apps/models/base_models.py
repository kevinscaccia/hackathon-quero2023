from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException, Request
from config import Config
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from fastapi import Depends
from typing import Union, List

#Model para representar usuario
class RegisteredUser(BaseModel):
    """An Authenticated user."""
    id: str = None
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None
    roles: List[str] = []

#Model para Tema
class Tema(BaseModel):
    id:str
    titulo:str
    texto_base:str
    data:str

class Temas(BaseModel):
    temas:List[Tema]


#Model request analise
class AnalysisRequest(BaseModel):
    titulo:str
    texto:str

#Model resposta analise
class Analysis(BaseModel):
    id:str
    nota_final:int
    comentarios:List[str] = []
    nota_criterios:List["Analysis.Criteria"]
    class Criteria(BaseModel):
        criterio:int
        nota:int