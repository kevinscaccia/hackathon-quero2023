
import json,threading,time,uuid
from psycopg2.errors import DuplicateTable
from concurrent.futures import thread
from ..models.Log import LogModel
from psycopg2.errors import UniqueViolation

_schemas = {
    "essays_themes":"""
        CREATE TABLE essays_themes (
            id uuid PRIMARY KEY DEFAULT gen_random_uuid(), 
            titulo VARCHAR(500),
            texto_base VARCHAR(5000),
            data TIMESTAMP DEFAULT NOW()
        )
    """,
    "essays":"""
        CREATE TABLE essays (
            id uuid PRIMARY KEY DEFAULT gen_random_uuid(), 
            titulo VARCHAR(500),
            texto_redacao VARCHAR(10000),
            theme_id uuid,
            CONSTRAINT fk_theme_id
                FOREIGN KEY(theme_id) 
                REFERENCES essays_themes(id)
        )
    """
}

class PostgreeHelper:
    
    def __init__(self, looker=None, con_pool=None, thread_lk=None) -> None:
        if type(looker) == None and not con_pool: raise Exception("É necessário uma lista para auditar ou uma pool de conexões")

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
    

    def insere_tema(self, titulo, texto_base) -> bool:
        #general
        if not self.conector:
            print("Impossivel inserir tema sem sessao instanciada!")
            return False
        
        try:
            _aux = self.conector.cursor()
            _aux.execute(
                '''
                    INSERT INTO essays_themes(titulo, texto_base)
                    VALUES ('{}', '{}');
                '''.format(titulo, texto_base)
            )
            self.conector.commit()
        except Exception as e:
            print(e)
            _aux.close()
            return False
        finally:
            _aux.close()

        return True

    def deleta_tema(self, id) -> bool:
        #general
        if not self.conector:
            print("Impossivel deletar tema sem sessao instanciada!")
            return False
        
        try:
            _aux = self.conector.cursor()
            _aux.execute(
                '''
                    DELETE FROM essays_themes WHERE id = '{}'
                '''.format(id)
            )
            self.conector.commit()
        except Exception as e:
            print(e)
            _aux.close()
            return False
        finally:
            _aux.close()

        return True
    
    def lista_tema(self):
        #general
        if not self.conector:
            print("Impossivel inserir tema sem sessao instanciada!")
            return False
        
        try:
            _aux = self.conector.cursor()
            _aux.execute(
                '''
                    SELECT titulo, texto_base, id 
                    FROM essays_themes
                '''.format(id)
            )
            saida = {"temas":[]}
            for v in _aux.fetchall():
                saida['temas'].append({"titulo":v[0], "texto_base":v[1],"id":v[2]})
            return saida
        except Exception as e:
            print(e)
            _aux.close()
        finally:
            _aux.close()

    def busca_tema(self,id):
        #general
        if not self.conector:
            print("Impossivel inserir tema sem sessao instanciada!")
            return False
        
        try:
            _aux = self.conector.cursor()
            _aux.execute(
                '''
                    SELECT *
                    FROM essays_themes
                    WHERE id = {}
                '''.format(id)
            )
            for v in _aux.fetchall():
                return saida['temas'].append({"titulo":v[0], "texto_base":v[1],"id":v[2]})
        except Exception as e:
            print(e)
            _aux.close()
        finally:
            _aux.close()
        

    def _insere_redacao(self, texto_redacao, titulo, theme_id) -> bool:
        #general
        if not self.conector:
            print("Impossivel inserir tema sem sessao instanciada!")
            return False
        
        try:
            _aux = self.conector.cursor()
            _aux.execute(
                '''
                    INSERT INTO essays(titulo, texto_redacao, theme_id)
                    VALUES ('{}', '{}', '{}');
                '''.format(titulo, texto_redacao, theme_id)
            )
            self.conector.commit()
        except Exception as e:
            print(e)
            _aux.close()
            return False
        finally:
            _aux.close()

        return True
    
    def _deleta_redacao(self, id) -> bool:
        #general
        if not self.conector:
            print("Impossivel inserir tema sem sessao instanciada!")
            return False
        
        try:
            _aux = self.conector.cursor()
            _aux.execute(
                '''
                    DELETE FROM essays WHERE theme_id = '{}'
                '''.format(id)
            )
            self.conector.commit()
        except Exception as e:
            print(e)
            _aux.close()
            return False
        finally:
            _aux.close()

        return True
    ##retorna


    def lista_qtd_redacao_por_tema(self):
        #general
        if not self.conector:
            print("Impossivel inserir tema sem sessao instanciada!")
            return False
        
        try:
            _aux = self.conector.cursor()
            _aux.execute(
                '''
                    select a.titulo, count(1) from essays_themes a
                        inner join essays b
                        on a.id = b.theme_id
                    group by a.titulo
                '''
            )
            return _aux.fetchall()
        except Exception as e:
            print(e)
            _aux.close()
            return False
        finally:
            _aux.close()
