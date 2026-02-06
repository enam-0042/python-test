from taskiq_redis import RedisAsyncResultBackend, RedisStreamBroker
from taskiq import InMemoryBroker, TaskiqEvents
import asyncio
import logging
logging.basicConfig(level=logging.DEBUG)

# Use Redis as the message carrier
try:
    result_backend = RedisAsyncResultBackend("redis://localhost:6379/0", result_ex_time=3600)
    
    broker = RedisStreamBroker("redis://localhost:6379/0",
                               ).with_result_backend(result_backend=result_backend)
    
    logging.info("Successfully Redis-broker initialized")
except Exception as e:
    logging.error(f"Failed to connect to Redis: {e}")
    logging.info("Falling back to InMemoryBroker")
    broker = InMemoryBroker()

@broker.on_event(TaskiqEvents.WORKER_STARTUP)
async def on_worker_startup(state):
    print("Worker is starting up...")

@broker.on_event(TaskiqEvents.WORKER_SHUTDOWN)
async def on_worker_shutdown(state):
    print("Worker is shutting down...")
