from typing import Any
from pathlib import Path
from cachetools import TTLCache
import json
from interfaces import NoSQLDatabase
from datetime import datetime, timedelta, timezone
import asyncio

class InMemoryTokenStore(NoSQLDatabase):
    def __init__(self, max_size=1000, ttl: int = 7200, cache_file_path: str = "tokens.json", save_after_n: int = 50):
        self.ttl = ttl
        self.cache = TTLCache(max_size, ttl=ttl)
        self.cache_file_path = cache_file_path
        self.save_after_n = save_after_n
        self._added_since_save = 0
        self._lock = asyncio.Lock()

        self.__load_tokens()

        # creating after loading so does not mess-up at startup
        Path(self.cache_file_path).parent.mkdir(parents=True, exist_ok=True)
        asyncio.create_task(self.__periodic_save())


    def __load_tokens(self):
        location = Path(self.cache_file_path)
        if not location.exists():
            return

        data = json.loads(location.read_text(encoding="utf-8"))

        now = datetime.now(timezone.utc)
        for token, expire_ts in data.items():
            expire_dt = datetime.fromisoformat(expire_ts)
            remaining_ttl = (expire_dt - now).total_seconds()
            if remaining_ttl > 0:
                self.cache[token] = True
                self.cache.ttl[token] = remaining_ttl

    async def __periodic_save(self, interval: int = 360):
        while True:
            await asyncio.sleep(interval)
            await self._save_tokens()

    async def _save_tokens(self):
        async with self._lock:
            data = {}
            now = datetime.now(timezone.utc)
            for token in self.cache:
                ttl_remaining = self.cache.get_ttl(token) if hasattr(self.cache, "get_ttl") else self.ttl
                expire_dt = now + timedelta(seconds=ttl_remaining)
                data[token] = expire_dt.isoformat()
            with open(self.cache_file_path, "w") as f:
                json.dump(data, f)
            self._added_since_save = 0


    def connect(self):
        pass

    def disconnect(self):
        asyncio.create_task(self._save_tokens())
        self.cache.clear()

    def set(self, key: str, value: str, exp: int = None):
        """Add a token with TTL (default to self.ttl)"""
        ttl = exp or self.ttl
        self.cache[key] = True
        self.cache.ttl[key] = ttl

        self._added_since_save += 1
        if self._added_since_save >= self.save_after_n:
            asyncio.create_task(self._save_tokens())

    def get(self, key: Any) -> bool:
        """Check if token exists (auto-deleted if expired)"""
        return key in self.cache
