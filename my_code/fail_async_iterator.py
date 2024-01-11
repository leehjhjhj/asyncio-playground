import asyncio
from bs4 import BeautifulSoup
import grequests
from timer_decorator import async_start_end_timer
from aiohttp import ClientSession

class TitleGetMachine:
    """
    이 이터레이터는 __anext__로 하나의 url에 대한 HTTP 요청을 하고 있다.
    따라서 동기식과 마찬가지로 URL에 순차적으로 요청을 보내는 것이다.
    이렇게 Network IO에 대해서는 `asyncio.gather()`를 이용하자. 
    """
    def __init__(self, urls: list[str]):
        self.urls = urls

    def __aiter__(self):
        self.target_urls = iter(self.urls)
        return self
    
    async def __anext__(self):
        try:
            url = next(self.target_urls)
        except StopIteration:
            raise StopAsyncIteration
        """
        여기서 response에서 await을 붙이는 이유는, response에는 헤더정보만 담겨있지 본문이 담겨있지 않다.
        이것은 aiohttp의 설계로 본문 내용이 매우 큰 것을 대비한 메모리 효율적이게 설계했단다.
        """
        async with ClientSession() as session:
            async with session.get(url) as response:
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                title = soup.title
                return title
            
@async_start_end_timer
async def main():
    urls = [
        'https://google.com',
        'https://naver.com',
        'https://daum.net',
        'https://github.com',
        'https://hufscheer.site',
    ]
    async for title in TitleGetMachine(urls):
        print(title)

asyncio.run(main())