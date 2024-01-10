import asyncio
import timeit

async def make_dough():
    print("피자 도우를 만들어보자.: {}".format(timeit.default_timer()))
    await asyncio.sleep(5.0)
    print("피자도우 완성!: {}".format(timeit.default_timer()))

async def add_topping(topping_type):
    print("{}을 조리하자.: {}".format(topping_type, timeit.default_timer()))
    await asyncio.sleep(3.0)
    print("{} 조리 완료!: {}".format(topping_type, timeit.default_timer()))
    return topping_type

async def make_pizza():
    print("피자를 만들어보자.: {}".format(timeit.default_timer()))
    task1 = asyncio.create_task(make_dough())
    task2 = asyncio.create_task(asyncio.sleep(7.0))
    topping = "새우"
    task3 = asyncio.create_task(add_topping(topping))
    await asyncio.gather(task1, task2)
    cooked_topping = await task3
    print("{} 피자 완성! 🍕: {}".format(cooked_topping, timeit.default_timer()))

async def main():
    start = timeit.default_timer()
    await asyncio.create_task(make_pizza())
    duration = timeit.default_timer() - start
    print("총 걸린 시간: {}".format(duration))

asyncio.run(main())

"""결과
피자를 만들어보자.: 0.053254625
피자 도우를 만들어보자.: 0.053314958
새우을 조리하자.: 0.053331208
새우 조리 완료!: 3.054716625
피자도우 완성!: 5.054652583
새우 피자 완성! 🍕: 7.054772916
총 걸린 시간: 7.001757791
"""