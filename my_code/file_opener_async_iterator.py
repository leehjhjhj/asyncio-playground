import aiofiles
import asyncio
from timer_decorator import async_start_end_timer

class AsyncLineReader:
    """
    비동기 이터레이터는 '데이터 묶음'을 처리할 때 유용하다고 한다.
    대용량 파일이나, 지속적으로 업데이트되는 데이터에 쓰인다.
    예를 들어 웹소켓을 통해 지속적으로 데이터를 전송받는 경우나
    대용량 파일을 조금씩 읽어야 하는 상황에서 비동기 이터레이터를 사용하면
    데이터를 조금씩 비동기적으로 처리할 수 있다.
    """
    def __init__(self, file):
        self.file = file

    def __aiter__(self):
        return self

    async def __anext__(self):
        line = await self.file.readline()
        if line:
            return line
        else:
            raise StopAsyncIteration

@async_start_end_timer
async def main():
    async with aiofiles.open('etc/large_file.txt', mode='r') as file:
        async for line in AsyncLineReader(file):
            pass
asyncio.run(main())
