import asyncio
import time

async def main():
    print("{} Hello!".format(time.ctime()))
    await asyncio.sleep(1.0)
    print("{} Goodbye!".format(time.ctime()))

def blocking():
    time.sleep(0.5)
    loop = asyncio.get_event_loop()
    print("{} Hello from a thread!".format(time.ctime()))
    return loop

loop = asyncio.get_event_loop()
task = loop.create_task(main())

loop.run_in_executor(None, blocking)
loop.run_until_complete(task)

pending = asyncio.all_tasks(loop=loop)
for task in pending:
    task.cancel()
group = asyncio.gather(*pending, return_exceptions=True)
loop.run_until_complete(group)
loop.close()