import time

def async_start_end_timer(func):
    async def timer(*args):
        start_time = time.perf_counter()
        print("타이머 시작: [{:.5f}s]".format(start_time))
        result = await func(*args)
        end_time = time.perf_counter() - start_time
        print("총 시간: [{:.5f}s]".format(end_time))
        if result is not None:
            return result
    return timer

def sync_start_end_timer(func):
    def timer(*args):
        start_time = time.perf_counter()
        print("타이머 시작: [{:.5f}s]".format(start_time))
        result = func(*args)
        end_time = time.perf_counter() - start_time
        print("총 시간: [{:.5f}s]".format(end_time))
        if result is not None:
            return result
    return timer
