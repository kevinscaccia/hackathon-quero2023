"""
[POC DATALAKE PROTHEUS]
Código de uso privado, reprodução proibida!
Todos direitos reservados à TOTVS ™
"""
import redis
class RedisHelper:
    """
    Classe para abstrair necessidades de integração com banco de cachê redis
    """
    def __init__(self) -> None:
        self.client = redis.Redis(host='svc-redis', port=6379, db=0)
        pass

    def set_cache(self, key, value, expire_time=None):
        """
        Define uma chave-valor no redis

        Parameters
        ----------
        key : str
            Chave para identificar o valor
        
        value : str
            Valor da chave
        
        expire_time : int
            Inteiro representando segundos de duração da chave-valor
        """
        if expire_time:
            self.client.setex(key, expire_time, value)
        else:
            self.client.set(key, value)

    def get_cache(self, key)-> str or None:
        """
        Recupera chave-valor do redis

        Parameters
        ----------
        key : str
            Chave identificadora do valor.
        
        Returns
        -------
        String utf-8 contendo valor da chave, caso exista,
                senão, retorna None.
        """
        cache_value = self.client.get(key)
        if cache_value:
            return cache_value.decode('utf-8')
        else:
            return None

    def delete_cache(self, key):
        """
        Remove chave-valor do redis

        Parameters
        ----------
        key : str
            Chave para ser removida do banco.
        """
        self.client.delete(key)