from pydantic import BaseModel
from uuid import uuid4

class LogModel(BaseModel):
    modo: str
    tipo: str
    txt: str
    transactionId:str = None
    tenantId:str = None
    latest_data_model:str = None
    pageload:dict = {}
    uuid:str = None
    def __init__(self, modo, tipo, txt, transactionId=None, tenantId=None, latest_data_model=None, pageload={}, uuid=None):
        super().__init__(modo=modo, tipo=tipo, txt=txt, transactionId=transactionId, tenantId=tenantId, latest_data_model=latest_data_model, pageload=pageload, uuid=uuid)
        self.modo = modo
        self.tipo = tipo
        self.txt = txt
        self.transactionId = transactionId
        self.tenantId = tenantId
        self.latest_data_model = latest_data_model
        self.pageload = pageload
        self.uuid = str(uuid4())
