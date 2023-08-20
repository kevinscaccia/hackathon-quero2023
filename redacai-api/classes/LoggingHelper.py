"""
[POC DATALAKE PROTHEUS]
Código de uso privado, reprodução proibida!
Todos direitos reservados à TOTVS ™
"""

import json,threading,time,uuid
from psycopg2.errors import DuplicateTable
from concurrent.futures import thread
from ..models.Log import LogModel
from psycopg2.errors import UniqueViolation

_schemas = {
    "general_logs":"""
        CREATE TABLE general_logs (
            id uuid PRIMARY KEY DEFAULT gen_random_uuid(), 
            transaction_id uuid,
            data TIMESTAMP DEFAULT NOW(), 
            tipo VARCHAR(100), 
            txt TEXT, 
            tenantId VARCHAR(300), 
            pageload JSONB
        )
    """,

    "interface_dotnet_messages":"""
        CREATE TABLE interface_dotnet_messages (
            id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
            transaction_id uuid,
            data TIMESTAMP DEFAULT NOW(),
            tipo VARCHAR(100),
            tenantId VARCHAR(300),
            txt TEXT,
            pageload JSONB
        )
    """,

    "carol_messages":"""
        CREATE TABLE carol_messages (
            id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
            transaction_id uuid,
            data TIMESTAMP DEFAULT NOW(),
            tipo VARCHAR(100),
            tenantId VARCHAR(300),
            latest_data_model VARCHAR(100),
            txt TEXT,
            pageload JSONB
        )
    """
}

class Auditor:
    """
    Classe para abstrair necessidades de auditabilidade das operações realizadas pela aplicação.
    
    Parameters
    ----------
    con_pool : psycopg2.pool
        Pool contendo conexões disponíveis com o banco
    
    looker : list
        Lista para observação dos logs a serem inseridos
            (Fila de prioridade)
    
    thread_lk : threading.Lock
        Objeto para controle de acesso ao objeto compartilhado (looker)
    
    Notes
    -----
    Esta classe tem dois modos de operação
        - Instancia fila de prioridade e monitora para inserção de logs ordenadas com controle de sessão
            Quando a classe recebe um objeto con_pool (Pool de conexões postgres)
        - Insere modelo pré definido LogModel na fila de prioridade para a posterior inserção do watcher
            Quando a classe recebe um looker para inserir e um thread_lk para controlar o acesso ao objeto da fila de prioridade
    
    """
    def __init__(self, looker=None, con_pool=None, thread_lk=None) -> None:
        if type(looker) == None and not con_pool: raise Exception("Uso incorreto da classe de logs! é necessário uma lista para auditar ou uma pool de conexões")

        if con_pool:
            self.con_pool = con_pool
            self.conector = self.con_pool.getconn()
            self.looker = []
            self.thread_lk = threading.Lock()
            if not self._setup_tabelas(): raise Exception("Impossivel realizar configuração do banco!")
        else:
            self.con_pool = None
            self.conector = None
            self.looker = looker
            self.thread_lk = thread_lk
        
        self.main_thread = None
        pass

    def _setup_tabelas(self) -> bool:
        """
        Realiza criação das tabelas caso não existam

        Returns
        -------
        bool : True caso sucesso,
                False caso erro.
        """
        #general
        if not self.conector:
            print("Impossivel configurar tabelas sem sessao instanciada!")
            return False
        
        for tabela,schema in _schemas.items():
            try:
                _aux = self.conector.cursor()
                _aux.execute(schema)
                self.conector.commit()
            except DuplicateTable as e:
                print(f"[i][{tabela}] já existe.")
                self.conector.rollback()
                continue
            except Exception as e:
                print(e)
                _aux.close()
                return False
            finally:
                _aux.close()
        return True
    
    def monitor_handler(self):
        self.main_thread = threading.Thread(target=self.monitor, args=())
        self.main_thread.start()

    def monitor(self):
        if not self.conector:
            print("Não é possivel monitorar sem sessão")
            return False
        
        if not self.thread_lk: self.thread_lk = threading.Lock()
        
        while True:
            if len(self.looker) > 0:
                self.thread_lk.acquire()
                _item = self.looker.pop(0)
                self.thread_lk.release()
                try:
                    self.log_banco(_item)
                except Exception as e:
                    print(f"[!] Erro log -> Item: {str(_item)}")
            time.sleep(30)

    def log(self, modo:str, tipo:str, txt:str, transactionId:str=None, tenantId:str = None, latest_data_model:str = None, pageload:dict = {})->str:
        _aux = LogModel(modo,tipo,txt,transactionId,tenantId,latest_data_model,pageload)
        self.looker.append(_aux)
        return _aux.uuid

    def log_banco(self, logItem:LogModel) -> bool:
        """
        Rotina para realizar log no banco

        Parameters
        ----------
        modo : str
            Modo de log,
                g = Geral
                d = DotNet Interface
                c = Carol
        
        transactionId : str
            UUID que identifica solicitação de predição que integra interfaces dotnet e python
                
        tipo : str
            Tipo do log, intrinseco ao modo.
        
        txt : str
            String principal do log
        
        tenantId : str
            Código identificador do tenant
            (Opcional) Dependendo do modo de log pode ser necessário.
        
        latest_data_model : str
            Versão do data model
            (Opcional) Dependendo do modo de log pode ser necessário
        
        pageload : dict
            Dicionario contendo pageload de uma requisição http
            (Opcional) Dependendo do modo de log pode ser necessário
        
        Returns
        -------
        Retorna string com uuid do log inserido
        """
    	
        if logItem.modo == "g":
            sql = f"INSERT INTO general_logs (id, transaction_id, tipo, txt, tenantId, pageload) VALUES ('{logItem.uuid}', %s, '{logItem.tipo}', '{logItem.txt}', '{logItem.tenantId}', %s);"
        elif logItem.modo == "d":
            sql = f"INSERT INTO interface_dotnet_messages (id, transaction_id, tipo, tenantId, txt, pageload) VALUES ('{logItem.uuid}', %s, '{logItem.tipo}', '{logItem.tenantId}', '{logItem.txt}', %s);"
        elif logItem.modo == "c":
            sql = f"INSERT INTO carol_messages (id, transaction_id, tipo, tenantId, latest_data_model, txt, pageload) VALUES ('{logItem.uuid}', %s, '{logItem.tipo}', '{logItem.tenantId}', '{logItem.latest_data_model}', '{logItem.txt}', %s);"
        _aux = self.conector.cursor()
        for k in range(3):
            try:
                _aux.execute(sql, [str(logItem.transactionId) if logItem.transactionId else None, json.dumps(logItem.pageload)])
                self.conector.commit()
                break
            except UniqueViolation as e:
                logItem.uuid = str(uuid.uuid4())
                self.conector.rollback()
                continue
            except Exception as e:
                print(f"[{type(e)}] erro logs->{e}\n\t sql -> {sql}")
                self.conector.rollback()
            finally:
                if k==2:
                    _aux.close()
                    return False
                continue
        _aux.close()
        return True
        


        