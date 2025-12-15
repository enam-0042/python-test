import asyncio
import time
import threading
from concurrent.futures import ProcessPoolExecutor
# #!/usr/bin/env python3
# # /home/gambler/Documents/test-fastapi/async_run.py

def now():
    return time.perf_counter()

# async def worker(name: str='tt', delay: float=5):
#     start = now()
#     print(f"{start:.4f} [{threading.current_thread().name}] START {name} sleeping {delay}s")
#     await asyncio.sleep(delay)
#     end = now()
#     print(f"{end:.4f} [{threading.current_thread().name}]  END  {name} elapsed {end - start:.4f}s")

# async def main():
#     t0 = now()
#     print(f"{t0:.4f} [event-loop] main() starting")
#     # create concurrent tasks
#     t1 = asyncio.create_task(worker("A", 1.0))
#     t2 = asyncio.create_task(worker("B", 1.5))
#     # wait for both to finish concurrently
#     await asyncio.gather(t1, t2)
#     t_end = now()
#     print(f"{t_end:.4f} [event-loop] main() finished (elapsed {t_end - t0:.4f}s)")

# ------this is coroutine functions
# couroutine are basically function whose execution can be pause
# 2 thing to remember
# coroutine function and coroutine obj
# co routine obj is the awaitable that gets returned when called
# the coroutine function
# cor... obj a is a genertor type in sense that it 
# can suspend execution and resume later
# but they are designed to work with eventloop

async def async_function(test_str):
    print('this is an async function ')
    await asyncio.sleep(2)
    return f'Async function result is {test_str}'

def fetch_data(param):
    print(f'start fetching data param- {param}' , flush=True)
    time.sleep(param)
    print(f'done fetching data param- {param}' , flush=True)
    return {f'data- {param}': param}


async def asyncio_corey():
    # print('corey')
    # await asyncio.sleep(2)
    # print('corey end')

# ----------------- future - low level object similiar js promise


    # loop = asyncio.get_running_loop()
    # future = loop.create_future()
    # print(future)

    # future.set_result(f'future result is {future}')
    # future_result = await future
    # print(future_result)


#------coroutine are defined with function async-def keyword
    # coroutine_obj = async_function("Test")
    # print(coroutine_obj)

    # coroutine_result = await coroutine_obj
    # print(coroutine_result)



# task are wrapped coroutine that can be execute independently by event loop
# task are how we run coroutine concurrently
# task are schedulable unit of work
#task keeps tab of when coroutine is paused and resumed, finish 
# successfully or with exception or got cancelled
# task uses futures under the hood to store result or exception 
# adds extra logic to run the coroutine and do the work we wanna do

    # task = asyncio.create_task(async_function("Task-wrapper  test"))
    # task = asyncio.create_task(async_function("Task-wrapper  test 2222"))

    # print(task)
    



    # ----------------- running blocking code in async function with to thread
    
    # run in thread pool executor
    task1  = asyncio.create_task(asyncio.to_thread(fetch_data, 3)   )
    task2  = asyncio.create_task(asyncio.to_thread(fetch_data, 6)   )  

    resutl1 = await task1
    print('process 1 fully completed')
    resutl2 = await task2
    print('process 2 fully completed')

    # run in process pool executor
    loop = asyncio.get_running_loop()
    with ProcessPoolExecutor() as executor:
        task1 = loop.run_in_executor(executor, fetch_data, 3)
        task2 = loop.run_in_executor(executor, fetch_data, 6)
        resutl1 = await task1
        print('process pool 1 fully completed')
        resutl2 = await task2
        print('process pool 2 fully completed')
    return [resutl1, resutl2] 

    # task_result = await task
    # print(task_result)
if __name__ == "__main__":
    start = now()
    print(f"{start:.4f} [main] Before asyncio.run (thread: {threading.current_thread().name})")
    # This call blocks the current thread until the coroutine completes
    # asyncio.run(worker())
    asyncio.run(asyncio_corey())
    print('fsfsfsf')
    # after = now()
    # print(f"{after:.4f} [main] After asyncio.run (total blocked {after - start:.4f}s)")
    # asyncio.sleep(7)

    # loop = asyncio.get_running_loop()
    # future = loop.create_future()
    # print(future)


    # # Run again to demonstrate asyncio.run can be called sequentially and blocks each time
    # print(f"{now():.4f} [main] Running asyncio.run a second time (single short task)...")
    # t0 = now()
    # asyncio.run(worker("C", 0.5))
    # t1 = now()
    # print(f"{t1:.4f} [main] After second asyncio.run (blocked {t1 - t0:.4f}s)")