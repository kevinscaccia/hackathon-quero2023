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


#Rotas default (erros)
router = APIRouter(
    responses={404: {"description": "nao implementado"}},
)

#instanciando jinja loader
templates = Jinja2Templates(directory="templates")

@router.get("/")
def index(request: Request):
    return templates.TemplateResponse("resource/home.html", {
        "request": request, 
        "current_user": RegisteredUser(username="test", roles=["admin"]),
        "config":Config()
    })

@router.get("/submit")
def submit(request:Request):
    return templates.TemplateResponse("resource/submit.html", {
        "request": request, 
        "current_user": RegisteredUser(username="test", roles=["admin"]),
        "config":Config()
    })

@router.get("/analyzer/{id}")
def analyzer(id:int, request:Request):
    print(f"Analisando {id}")
    return templates.TemplateResponse("resource/analyzer.html", {
        "request": request, 
        "current_user": RegisteredUser(username="test",roles=["admin"]),
        "config":Config()
    })