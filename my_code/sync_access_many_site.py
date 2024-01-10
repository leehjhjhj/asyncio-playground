import asyncio
import requests
from bs4 import BeautifulSoup
import timeit
from timer_decorator import sync_start_end_timer

def blocking_access_site(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.title
    return title

@sync_start_end_timer
def main():
    urls = [
        'https://google.com',
        'https://naver.com',
        'https://daum.net',
        'https://github.com',
    ]
    titles = [blocking_access_site(url) for url in urls]
    print(*titles)

main()