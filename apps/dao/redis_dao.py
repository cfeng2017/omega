import redis
from apps.model.common.logger import Logger
from apps import config


class OmegaRedis:

    def __init__(self):
        try:
            conn = self.connect()
            if not conn:
                self._alive = False
            conn.ping()
        except redis.ConnectionError:
            Logger.error("Redis Server is Unreachable!")
            self._alive = False
        else:
            self._alive = True
        finally:
            self.disconnect(conn)

    @classmethod
    def connect(cls):
        rserver = getattr(config, 'REDIS_SERVER', None)
        if not rserver:
            Logger.error("settings.py's config about Redis Server is wrong!")
            return False
        pool = redis.ConnectionPool(host=rserver['host'], port=rserver['port'])
        return redis.StrictRedis(connection_pool=pool, socket_timeout=0.1, socket_connect_timeout=0.2)

    @classmethod
    def disconnect(cls, conn):
        redis.ConnectionPool(conn).disconnect()

    @classmethod
    def check_memory(cls):
        return True

    @classmethod
    def available(cls):
        """
        Is redis server available? Redis server is readable( and writable).
        """
        return True

    @classmethod
    def delete(cls, key):
        oredis = OmegaRedis()
        if oredis._alive:
            conn = oredis.connect()
            conn.delete(key)

