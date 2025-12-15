# import asyncio



# dicts={}
# dicts['tts']='hola'
# dicts['tts']='yyy'
# # print(dicts['tts'])

# async def foo():
#     print("foo started")
#     await asyncio.sleep(2)
#     print("foo finished")

# async def main():
#     asyncio.create_task(foo())
#     print("task created")
#     await asyncio.sleep(1)  # give loop a chance to run foo
#     print("main still running")
#     await task

# asyncio.run(main())





# /// what if no task=asy....


import asyncio
import time
def hello_boss(x):
    tm= time.time()
    while time.time() - tm <x :
        pass

    print(time.time()-tm, ' passed' )
async def bad_task():
    print('asyncio task created')
    await asyncio.sleep(2)
    print('nothing happened yyyy')
    raise ValueError("Something went wrong!")

async def main():
    hello_boss(5)
    asyncio.create_task(bad_task())  # no reference kept
    await asyncio.sleep(1)           # give it time to run

asyncio.run(main())
