from contextlib import asynccontextmanager
import requests
import asyncio

@asynccontextmanager
async def web_page(url):
    loop = asyncio.get_running_loop()
    data = await loop.run_in_executor(None, requests.get, url)
    yield data.status_code
    await asyncio.sleep(1.0)
    print('스탯 업데이트 함수 호출 모형')

async def main():
    urls = [
        'https://google.com',
        'https://naver.com',
        'https://daum.net',
        'https://github.com',
    ]

    tasks = [web_page(url).__aenter__() for url in urls]

    for task in asyncio.as_completed(tasks):
        data = await task
        print(data)

asyncio.run(main())
