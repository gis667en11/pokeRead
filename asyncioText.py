import asyncio
import time
x = 0

async def nested():
    global x
    while True:
        print(f"nested {x}")
        await asyncio.sleep(3)
        x += 1

async def mainEcho():
    while True:
        print("Main Echo")
        await asyncio.sleep(1)

async def main():

    while True:
        # Schedule nested() to run soon concurrently
        # with "main()".
        task = asyncio.create_task(nested())
        task2 = asyncio.create_task(mainEcho())

        # "task" can now be used to cancel "nested()", or
        # can simply be awaited to wait until it is complete:
        while True:
            print("testing")
            await asyncio.sleep(1)
        

asyncio.run(main())