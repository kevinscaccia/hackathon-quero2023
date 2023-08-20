
from fastapi import FastAPI, Request
from fastapi.middleware.gzip import GZipMiddleware
from .routers import redacai_utils 

from psycopg2.extensions import parse_dsn
from psycopg2 import pool

import os, redis

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
    request.state.pg_pool = pool.SimpleConnectionPool(1, 20, user="postgres",
                                                         password="a274-e535-472b-8ad",
                                                         host="localhost",
                                                         port="32770",
                                                         database="postgres") 


    response = await call_next(request)
    return response


#Instanciando rotas de controllers
app.include_router(redacai_utils.router)


#Rotas de heartbeat
@app.get("/_/health/liveness", include_in_schema=False)
async def health_check():
    return {'status':'ok'}

@app.get("/_/health/readiness", include_in_schema=False)
async def health_readiness():
    return {'status':'ok'}