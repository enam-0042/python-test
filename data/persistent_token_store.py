from diskcache import Cache
from utils.singleton import singleton
from interfaces import NoSQLDatabase

@singleton
class PersistentTokenStore(NoSQLDatabase):

    def __init__(self, cache_dir="db"):
        self.cache = Cache(directory=cache_dir)

    def connect(self):
        pass

    def disconnect(self):
        pass
    def set(self, key: str, value: bool = True, exp: int = 7200):
        self.cache.set(key, value, expire=exp)

    def get(self, key: str) -> bool:
        return self.cache.get(key, None) is not None

    def close(self):
        self.cache.close()