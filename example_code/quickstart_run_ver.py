import asyncio
import time
from concurrent.futures import ThreadPoolExecutor

async def main():
    print(f"{time.ctime()} Hello!")
    await asyncio.sleep(1.0)
    print(f"{time.ctime()} Goodbye!")

def blocking():
    time.sleep(0.5)
    print(f"{time.ctime()} Hello from a thread!")

async def main_wrapper():
    # 메인 코루틴 생성
    task = asyncio.create_task(main())

    # 별도의 스레드에서 blocking 함수 실행
    loop = asyncio.get_running_loop()
    loop.run_in_executor(None, blocking)

    # 메인 코루틴 완료까지 대기
    await task

    # 아직 미완료인 모든 태스크 취소
    pending = asyncio.all_tasks()
    pending.discard(asyncio.current_task())
    for task in pending:
        task.cancel()

    # 취소된 태스크들의 완료를 기다림
    await asyncio.gather(*pending, return_exceptions=True)

asyncio.run(main_wrapper())
