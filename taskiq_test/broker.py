import taskiq_redis
from taskiq import InMemoryBroker, AsyncBroker

# Use Redis as the message carrier
broker = taskiq_redis.RedisAsyncBroker("redis://localhost:6379")