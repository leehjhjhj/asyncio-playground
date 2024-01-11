import aiofiles
import asyncio
from timer_decorator import async_start_end_timer

async def async_line_reader(file):
    async with aiofiles.open(file, mode='r') as file:
        while True:
            line = await file.readline()
            if not line:
                break
            yield line

@async_start_end_timer
async def main():
    file = 'etc/large_file.txt'
    async for line in async_line_reader(file):
        print(line)

asyncio.run(main())
