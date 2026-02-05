from taskiq import InMemoryBroker
import asyncio

broker = InMemoryBroker()


@broker.task
async def add_one(value: int) -> int:
    await asyncio.sleep(2)
    return value + 7


async def main():
    await broker.startup()
    task = await add_one.kiq(1)

    result = await task.wait_result(timeout=5)
    print(f"Result: {result}")

    if not result.is_err:
        print(f"Success: {result.return_value}")
    else:
        print(f"Error: {result.exception}")
    await broker.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
