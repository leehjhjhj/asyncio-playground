import asyncio
import requests
from bs4 import BeautifulSoup
import timeit
from timer_decorator import async_start_end_timer

def blocking_access_site(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.title
    return title

@async_start_end_timer
async def main():
    urls = [
        'https://google.com',
        'https://naver.com',
        'https://daum.net',
        'https://github.com',
    ]
    loop = asyncio.get_running_loop()
    futures = [loop.run_in_executor(None, blocking_access_site, url) for url in urls]
    titles = await asyncio.gather(*futures)
    print(*titles)

asyncio.run(main())