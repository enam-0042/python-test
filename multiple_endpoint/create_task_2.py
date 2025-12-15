import asyncio

async def background_task(delay):
    print(f"Task started, sleeping for {delay} seconds...")
    await asyncio.sleep(delay)
    print(f"Task finished after {delay} seconds.")
    return f"Result after {delay}s"

async def main():
    # 1. Create and schedule the tasks
    task1 = asyncio.create_task(background_task(3), name='Task_A') 
    task2 = asyncio.create_task(background_task(1), name='Task_B')

    print("Tasks created. Continuing main() coroutine.")
    
    # Execution will switch between tasks here as they hit 'await' points.

    # 2. Await the tasks to get the results and ensure they complete
    result1 = await task1
    result2 = await task2
    
    print(f"Task 1 result: {result1}")
    print(f"Task 2 result: {result2}")

if __name__ == "__main__":
    # This runs the top-level coroutine and manages the event loop
    # In Python 3.7+
    asyncio.run(main())