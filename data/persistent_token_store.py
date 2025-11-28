from diskcache import Cache
from utils.singleton import singleton
from interfaces import NoSQLDatabase

@singleton
class PersistentTokenStore(NoSQLDatabase):

    def __init__(self, cache_dir="db", ttl=7200):
        self.cache = Cache(directory=cache_dir)
        self.default_ttl = ttl

    def connect(self):
        pass

    def disconnect(self):
        pass
    def set(self, key: str, value: bool = True, exp: int = None):
        ttl = exp or self.default_ttl
        self.cache.set(key, value, expire=ttl)

    def get(self, key: str) -> bool:
        return self.cache.get(key) is not None

    def close(self):
        self.cache.close()