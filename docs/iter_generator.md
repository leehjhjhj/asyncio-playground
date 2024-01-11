# 이터레이터와 제네레이터의 올바른 이해
## 이터레이터
```python
class A:
    def __iter__(self):
        self.x = 0
        return self
    
    def __next__(self):
        if self.x > 2:
            rais StopIteration
        else:
            self.x += 1
            return self.x

for i in A():
    print(i)
1
2
3
```
- 값을 차례대로 꺼낼 수 있는 객체
- 이터러블(iterable): 순회 가능한 객체. 리스트, 튜플, 문자열 등이 속하며 이 객체들은 `__iter__()` 매직 메서드가 있고, 이를 통해서 이터레이터를 반환
- 이터레이터(iterator): `__next__()` 매직 메서드를 구현한 객체. 이 메서드를 호출하면 이터레이터의 다음 항목을 반환한다.  `__iter__()`도 있기 때문에 모든 이터레이터는 이터레이블이다.
- A는 단지 `a = A()`를 할 시 A의 인스턴스가 되지만 `__iter__()`가 호출되면 (for문과 같이) 이터레이터가 반환된다. 하지만 이것은 언제나 인스턴스에 `__next__()` 메서드가 있어야 한다.
- 즉 위의 A 클래스는 본인이 `__next__()`도 가지고 있기 때문에, iter 메소드에서 자기 자신을 반환하면 그것이 이터레이터이다. 따라서 이터레이터이자 이터러블이다.

## 비동기 이터레이터
- `__aiter__()`와 `__anext__()`를 사용
- `__anext()__`는 async def로 생성한다. `__aiter__()` 에는 붙지 않는다.

## 비동기 제네레이터
```python
import asyncio
from aioredis import create_redis

async def main():
    redis = await create_redis(('localhost', 6379))
    keys = ['Americas', 'Africa', 'Europe', 'Asia']

    async for value in one_at_a_time(redis, keys):
        await do_someting_with(value)
    
    async def one_at_a_time(redis, keys):
        for k in keys:
            value = await redis.get(k)
            yield value

asyncio.run(main())
```
- async for문이 실행되면 먼저 `one_at_a_time()`이 동작한다.
- 그러면 `one_at_a_time()`의 for문이 돌면서 redis 객체를 얻어낸다
- yield에 오면 value 값을 `async for`의 `value`에 반환하고 일시정지 시킨다.
- `async for`의 로직이 수행된다. 이때 `do_someting_with`도 코루틴이니 await을 통해서 비동기로 처리한다.
- 그 후, 내부코드(do_someting_with)가 완료되면(await이니 호출하고 넘어가겠지만) 다시 `one_at_a_time()`을 호출한다.
- `one_at_a_time()`가 호출되면 아까 멈춰있던 yield 이후의 로직이 수행되며, 다시 루프가 돌아간다.
- **만약에 제네레이터에 return이 있으면 무조건 `StopIteration`예외가 발생한다.** -> 그러면 제네레이터가 끝난다.