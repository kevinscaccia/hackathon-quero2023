from models.base_models import Temas, Tema, Analysis
from random import randint
from datetime import datetime,timedelta
import requests as req
def tema_gen(i):
    output = []
    for j in range(i):
        output.append(Tema(id=j, titulo=f"tema{j}", texto_base=f"texto_base{j}", data=f"{(datetime.now()+timedelta(days=j)).strftime('%Y-%m-%d')}"))
    return output

class bk:
    def __init__(self) -> None:
        self.base = f"http://localhost:8000"
        pass

    def request_temas(self) -> Temas:
        """Obtem lista de temas disponiveis"""
        v = req.get(f"{self.base}/listThemes").json()
        return v

    def request_analysis(self,titulo:str, texto:str, tema:str) -> str:
        """Solicita analise do modelo e retorna id da analise"""
        data = {
            "titulo": titulo,
            "texto": texto,
            "tema_id":tema
        }
        # Fazendo a requisição POST
        response = req.post(f"{self.base}/submit/", json=data)
        return response.json() if response.status_code == 200 else False
    
    def retrieve_analysis(self,id:int) -> Analysis:
        """Recupera informações da gerada no banco"""
        #TODO - IMPLEMENTAR REQUEST
        return Analysis(id=1, nota_final=760, comentarios=['coment1', 'coment2'], nota_criterios=[Analysis.Criteria(criterio=1, nota=120), Analysis.Criteria(criterio=2, nota=120), Analysis.Criteria(criterio=3, nota=120), Analysis.Criteria(criterio=4, nota=120), Analysis.Criteria(criterio=5, nota=120)])

    def request_tema(self, id) -> Tema:
        #TODO - IMPLEMENTAR REQUEST
        return tema_gen(1)[0]
    