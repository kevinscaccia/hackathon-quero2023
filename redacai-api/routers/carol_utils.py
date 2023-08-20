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
from ..classes.RedisHelper import RedisHelper
from ..models.TenantToUpdateRequest import TenantToUpdateRequest
from ..models.TenantReportRequest import TenantReportRequest
from ..models.DataModelExtractorRequest import DataModelExtractorRequest

router = APIRouter()

@router.post("/updateApp/", summary="Atualiza versão do Carol App nas tenants",tags=["Cockpit"], description="Realiza a expedição de novas versões dos Carol Apps nos tenants inputados")
async def app_updater(body_params:TenantToUpdateRequest, req:Request, appsToUpdate: str = Header(alias='appsToUpdate', description='Apps para serem expedidos nos clientes passados')):
    """
    Rota para expedição de nova versão do app em tenants
    """
    try:
        logger = Auditor(looker=req.state.auditor_queue, thread_lk=req.state.auditor_lock)
        updater_id = str(uuid.uuid4())

        logger.log(modo='g', tipo='INFO', txt=f"Expedicao de apps para {len(body_params.tenant_list)} tenants concluida", transactionId=updater_id)
        return {"success": True}
    except Exception as e:
        print(traceback.format_exc())
        logger.log(modo='c', tipo='ERR', txt=f'Erro desconhecido na expedicao de apps {e} STACK -> {traceback.format_exc()}', pageload={"header":dict(req.headers), "body":body_params})
        raise HTTPException(status_code=500, detail=f"Erro ao expedir apps!")

@router.post("/report/", summary="Processa relatório de tabelas do cliente",tags=["Monitoramento"], description="Processa relatório de tabelas dos clientes em suas respectivas tenants")
async def reporter_list(body_params:TenantReportRequest, req:Request, bg_worker:BackgroundTasks, force:int=Query(0, description='1 para forçar execução do relatório (Cancela execução existente)')):
    """
    Rota de geração de relatório de tabelas para vários tenants

    Parameters
    ----------
    body_params : models.TenantReportRequest
        Objeto para autenticar e realizar relatório
    
    req : fastapi.Request
        Request cru para coleta de métricas de log
    
    bg_worker : fastapi.BackgroundTasks
        Controlador para executar relatórios de forma assíncrona

    Returns
    -------
    UUID chave única do relatório solicitado
        {
            "transaction_id":<uuid>
        }

    """
    try:
        logger = Auditor(looker=req.state.auditor_queue, thread_lk=req.state.auditor_lock)
        _r = RedisHelper()
        if force: _r.delete_cache("lock-report-orgs")
        report_id = str(uuid.uuid4())
        aux = logger.log(modo='c', tipo='INFO', transactionId=report_id, txt=f"Relatorio de tabelas solicitado para {len(body_params.tenant_list)} tenants", pageload={"header":dict(req.headers), "body":str(body_params)})
        _actualtoken = _r.get_cache("lock-report-orgs")

        if _actualtoken:
            aux = logger.log(modo='c', tipo='INFO', transactionId=report_id, txt=f"Relatorio de tabelas já em processamento! {_actualtoken}", pageload={"header":dict(req.headers), "body":str(body_params)})
            return {
                "transaction_id":_actualtoken
            }
        if not body_params:
            raise HTTPException(status_code=500, detail=f"Body da requisição vazio!")
        
        bg_worker.add_task(_c.gera_relatorio_unico, report_id, body_params)
        _r.set_cache("lock-report-orgs", report_id)

        return {
            "transaction_id": report_id,
        }
    except Exception as e:
        print(traceback.format_exc())
        logger.log(modo='c', tipo='ERR', txt=f'Erro na aplicacao report {e}')
        
@router.get("/report/", summary="Processa relatório de tabelas no Tenant Unificado",tags=["Monitoramento"], description="Processa relatório de tabelas dos clientes no Tenant Unificado")
async def reporter(req:Request, bg_worker:BackgroundTasks, force:int=Query(0, description='1 para forçar execução do relatório (Cancela execução existente)')):
    """
    Rota de geração de relatório no Tenant Unificado
    """
    try:
        logger = Auditor(looker=req.state.auditor_queue, thread_lk=req.state.auditor_lock)
        _r = RedisHelper()
        if force: _r.delete_cache("lock-report-unif")
        aux = logger.log(modo='c', tipo='INFO', txt='Relatorio para tenant unificado solicitado', pageload={"header":dict(req.headers)})
        report_id = str(uuid.uuid4())
        _actualtoken = _r.get_cache("lock-report-unif")
        if _actualtoken:
            aux = logger.log(modo='c', tipo='INFO', transactionId=report_id, txt=f"Relatorio de tabelas já em processamento! {_actualtoken}", pageload={"header":dict(req.headers)})    
            return {
                "transaction_id":_actualtoken
            }
        bg_worker.add_task(_c.gera_relatorio_unificado, report_id)
        _r.set_cache("lock-report-unif", report_id)

        return {
            "transaction_id": report_id,
        }
    except Exception as e:
        print(traceback.format_exc())
        logger.log(modo='g', tipo='ERR', txt=f'Erro na aplicacao report {e}')
        

@router.post("/extract/", summary="Extrai dados da Carol", tags=["Cockpit"], description="Executa extração de Data Model na plataforma TOTVS Carol")
async def extractor(body_params:DataModelExtractorRequest, req:Request, bg_worker:BackgroundTasks):
    """
    Rota de extração de Data Models

    Parameters
    ----------
    body_params : models.TenantReportRequest
        Objeto para autenticar e realizar relatório
    
    req : fastapi.Request
        Request cru para coleta de métricas de log
    
    bg_worker : fastapi.BackgroundTasks
        Controlador para executar relatórios de forma assíncrona

    Returns
    -------
    UUID chave única do relatório solicitado
        {
            "transaction_id":<uuid>
        }
    """
    try:
        logger = Auditor(looker=req.state.auditor_queue, thread_lk=req.state.auditor_lock)
        _r = RedisHelper()
        report_id = str(uuid.uuid4())
        aux = logger.log(modo='c', tipo='INFO', transactionId=report_id, txt=f"Extração de DataModel solicitado {len(body_params.dms_list)} data models",pageload={"header":dict(req.headers), "body":body_params.json()})
        _actualtoken = _r.get_cache("lock-extractions")

        if _actualtoken:
            aux = logger.log(modo='c', tipo='INFO', transactionId=report_id, txt=f"Extração de Data Models já em processamento! {_actualtoken}", pageload={"header":dict(req.headers), "body":body_params.json()})
            
            return {
                "transaction_id":_actualtoken
            }
        if not body_params:
            raise HTTPException(status_code=500, detail=f"Body da requisição vazio!")
        from datetime import datetime
        print(f"{datetime.now()} - Iniciado descida")
        bg_worker.add_task(_c.extrator, body_params, report_id, True)
        _r.set_cache("lock-extractions", report_id)

        return {
            "transaction_id": report_id,
        }
    except Exception as e:
        print(traceback.format_exc())
        logger.log(modo='c', tipo='ERR', txt=f'Erro na aplicacao report {e}')


    # router.get("/themeList/", summary="Retorna lista de temas disponíveis")
    # def submitter(req:Request):
    #     try:
    #         pass
    #     except Exception as e:
    #         pass

    # @router.get("/essayQuantityByTheme/{id}", summary="Retorna quantidade de redações por tema")
    # def submitter(body_params:, req:Request, bg_worker:BackgroundTasks):
    #     try:
    #         pass
    #     except Exception as e:
    #         pass

    # @router.post("/submit/", summary="Submete uma redação para avaliação")
    # def submitter(body_params:SubmitModelExtractorRequest, req:Request):
    #     try:
    #         pass
    #     except Exception as e:
    #         pass