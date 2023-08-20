
from fastapi import FastAPI, Request
from fastapi.middleware.gzip import GZipMiddleware
from .routers import carol_utils
from .classes.LoggingHelper import Auditor

from pycarol import Carol, ApiKeyAuth
from pycarol.bigquery import BQ

from psycopg2.extensions import parse_dsn
from psycopg2 import pool

import os, redis

#Iniciando Pool de conexões
#pool_pg = pool.ThreadedConnectionPool(
#    minconn=int(os.environ['PY_DB_POOL_MIN_CON']),
#    maxconn=int(os.environ['PY_DB_POOL_MAX_CON']),
#    **parse_dsn(os.environ['PY_DB_CONNECTION'])
#)
#if pool_pg.closed: raise Exception("Falha ao conectar ao banco de dados!")


#Inicialização
#print("[i] Conexao com o banco realizada com sucesso")
#sessao_redis = redis.Redis(host='svc-redis', port=6379, db=0)
#print("[i] Conexao com o cache realizada")
#sessao_carol = Carol(domain=os.environ['PY_CAROL_DOMAIN'], app_name=os.environ['PY_CAROL_APPNAME'], auth=ApiKeyAuth(api_key=os.environ['PY_CAROL_CONNECTOR_API_TOKEN']), connector_id=os.environ['PY_CAROL_CONNECTOR_ID'], organization=os.environ['PY_CAROL_ORGANIZATION'], host="totvstechfindev.carol.ai")
#sessao_bq = BQ(sessao_carol)
#print("[i] Conexao com a Carol estabelecida")
#_auditor = Auditor(con_pool=pool_pg)
#_auditor.monitor_handler()
#print("[i] Thread de logs instanciada!")

#Customização Swagger
app = FastAPI(
    title="redac-ai", 
    version="0.0.1",
    docs_url="/swagger"
)

#Middleware para compressão de pacotes (útil para transferências volumosas)
app.add_middleware(GZipMiddleware, minimum_size=3500)

#Middleware para compartilhamento de sessões
@app.middleware('http')
async def add_sessao_state(request:Request, call_next):
    """
    Rotina do middleware customizado para adicionar ao state da requisição a sessão do PG Admin

    Parameters
    ----------
    request : FastAPI.Request
        Request que chega na API.
    
    call_next : function
        Rotina do endpoint, passada automaticamente pelo FastAPI
    
    Returns
    -------
    Response : FastAPI.Response
        Resposta HTTP para saída
    """
    response = await call_next(request)
    return response


#Instanciando rotas de controllers
app.include_router(carol_utils.router)


#Rotas de heartbeat
@app.get("/_/health/liveness", include_in_schema=False)
async def health_check():
    return {'status':'ok'}

@app.get("/_/health/readiness", include_in_schema=False)
async def health_readiness():
    return {'status':'ok'}