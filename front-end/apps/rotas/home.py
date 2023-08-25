from __future__ import annotations
from typing import Annotated
from fastapi import APIRouter, Request, Form
from config import Config
from fastapi.templating import Jinja2Templates
from models.base_models import RegisteredUser, AnalysisRequest
from api_wrapper import bk
from starlette.responses import RedirectResponse
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
        "objects": bk().request_temas(),
        "current_user": RegisteredUser(username="test", roles=["admin"]),
        "config":Config()
    })

@router.get("/submit/{id_tema}")
def submit(id_tema:str, request:Request):
    r = bk().request_tema(id_tema)
    return templates.TemplateResponse("resource/submit.html", {
        "request": request, 
        "tema":r,
        "current_user": RegisteredUser(username="test", roles=["admin"]),
        "config":Config()
    })

@router.post("/analyzer/{id_tema}/{id}")
def analyzer(id:str, id_tema:str, request:Request):
    print(f"[i] Buscando {id}")
    redacao = bk().retrieve_analysis(id)
    tema = bk().request_tema(id_tema)
    return templates.TemplateResponse("resource/analyzer.html", {
        "request": request,
        "tema":tema,
        "redacao":redacao,
        "current_user": RegisteredUser(username="test",roles=["admin"]),
        "config":Config()
    })

@router.post("/submit/{id_tema}")
def submite_analysis(id_tema:str, txtRedacao:Annotated[str, Form()], txtTituloRedacao:Annotated[str, Form()], request:Request):
    _h = bk()
    id_analise = _h.request_analysis(txtTituloRedacao, txtRedacao, id_tema)
    return RedirectResponse(url=router.url_path_for("analyzer", id=id_analise, id_tema=id_tema))