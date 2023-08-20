"""
[POC DATALAKE PROTHEUS]
Código de uso privado, reprodução proibida!
Todos direitos reservados à TOTVS ™
"""
import uuid, traceback

from fastapi import APIRouter, Request, HTTPException, BackgroundTasks, Query, Header
from typing import List,Dict
from pycarol import Carol, ApiKeyAuth
from pycarol.apps import Apps

from ..classes.LoggingHelper import Auditor
from ..models.SubmitModelExtractorRequest import SubmitModelExtractorRequest

router = APIRouter()


@router.get("/themeList/", summary="Retorna lista de temas disponíveis")
async def theme_list(req:Request):
    try:
        return {"Success":True}
    except Exception as e:
        print(traceback.format_exc())
        #logger.log(modo='g', tipo='ERR', txt=f'Erro na aplicacao report {e}')

@router.get("/essayQuantityByTheme/{id}", summary="Retorna quantidade de redações por tema")
async def essayQuantityByTheme(id:int):
    try:
        return {"Success":True}

    except Exception as e:
        print(traceback.format_exc())

# @router.post("/submit/", summary="Submete uma redação para avaliação")
# async def submitter(body_params:SubmitModelExtractorRequest, req:Request):
#     try:
#         return {"Success":True}
        
#     except Exception as e:
#         print(traceback.format_exc())
#         #logger.log(modo='g', tipo='ERR', txt=f'Erro na aplicacao report {e}')