
import uuid, traceback


from fastapi import APIRouter, Request, HTTPException, BackgroundTasks, Query, Header
from typing import List,Dict

from ..classes.LoggingHelper import Auditor
from ..classes.PostgreeHelper import PostgreeHelper
from ..models.SubmitRequestModel import SubmitRequestModel
from ..models.EssayModel import EssayModel


router = APIRouter()


### Theme and Essays CRUD
@router.post("/insertTheme/{titulo}/{texto_base}", summary="Insere tema de redação", tags=["Essay CRUD"])
async def theme_creator(titulo:str, texto_base:str, req:Request):
    try:
        _p = PostgreeHelper(con_pool=req.state.pg_pool)

        return {
                "Success": _p.insere_tema(titulo, texto_base)
                }
        
    except Exception as e:
        print(traceback.format_exc())
        #logger.log(modo='g', tipo='ERR', txt=f'Erro na aplicacao report {e}')

@router.delete("/deleteTheme/{id}", summary="Delete tema de redação", tags=["Essay CRUD"])
async def theme_delete(id:str, req:Request):
    try:
        _p = PostgreeHelper(con_pool=req.state.pg_pool)

        return {
                "Success": _p.deleta_tema(id)
                }
        
    except Exception as e:
        print(traceback.format_exc())
        #logger.log(modo='g', tipo='ERR', txt=f'Erro na aplicacao report {e}')


@router.get("/listThemes/", summary="Retorna lista de temas disponíveis", tags=["Essay CRUD"])
async def theme_list(req:Request):
    try:
        _p = PostgreeHelper(con_pool=req.state.pg_pool)
        
        return _p.lista_tema()
    
    except Exception as e:
        print(traceback.format_exc())

@router.post("/insertEssay/", summary="Insere uma redação", tags=["Essay CRUD"])
async def essay_creator(redac:EssayModel, req:Request):
    try:
        _p = PostgreeHelper(con_pool=req.state.pg_pool)

        return {
                "Success": _p._insere_redacao(redac.texto_redacao, redac.titulo, redac.theme_id, redac.nota_final, redac.crit_1_nota, redac.crit_2_nota, redac.crit_3_nota, redac.crit_4_nota, redac.crit_5_nota, redac.comentarios)
                }
        
    except Exception as e:
        print(traceback.format_exc())
        #logger.log(modo='g', tipo='ERR', txt=f'Erro na aplicacao report {e}')

@router.delete("/deleteEssay/{id}", summary="Deleta redação", tags=["Essay CRUD"])
async def essay_delete(id:str, req:Request):
    try:
        _p = PostgreeHelper(con_pool=req.state.pg_pool)

        return {
                "Success": _p._deleta_redacao(id)
                }
        
    except Exception as e:
        print(traceback.format_exc())
        #logger.log(modo='g', tipo='ERR', txt=f'Erro na aplicacao report {e}')

@router.get("/essayQuantityByTheme", summary="Retorna quantidade de redações por tema", tags=["Cockpit"])
async def essayQuantityByTheme(req:Request):
    try:
        _p = PostgreeHelper(con_pool=req.state.pg_pool)
        
        return _p.lista_qtd_redacao_por_tema()
    
    except Exception as e:
        print(traceback.format_exc())

    except Exception as e:
        print(traceback.format_exc())

@router.get("/theme/{id}", summary="Submete uma redação para avaliação", tags=["Cockpit"])
def theme_search(id, req:Request):
    """Rotina para recuperar id"""
    try:
        _p = PostgreeHelper(con_pool=req.state.pg_pool)
        return _p.busca_tema(id)
    except Exception as e:
        print(traceback.format_exc())


@router.get("/essay/{id}")
def essay_search(id, req:Request):
    try:
        _p = PostgreeHelper(con_pool=req.state.pg_pool)
        return _p.busca_analise(id)
    except Exception as e:
        print(traceback.format_exc())

@router.post("/submit/", summary="Submete uma redação para avaliação", tags=["Cockpit"])
async def submitter(body_params:SubmitRequestModel, req:Request):
    try:
        print(body_params)
        #TODO MANDA PARA MODELO
        #TODO CADASTRA
        import uuid
        return {"id_analise":str(uuid.uuid4()), "nota_final":1000, "nota_criterios":[{"criterio":1, "nota":200}], "comentarios":['a','b','c']}
    except Exception as e:
        print(traceback.format_exc())
        #logger.log(modo='g', tipo='ERR', txt=f'Erro na aplicacao report {e}')