## 코루틴은 무엇인가?
### 코루틴 타입
```python
async def f():
    return 123

print(type(f)) # <class 'function'>

f = f()
print(type(f)) # <class 'coroutine'>
```
- `f()`는 `코루틴`이 아니라 `코루틴 함수`이다.
- 이는 제네레이터도 마찬가지인데, yield가 들어간 함수는 `제네레이터 함수`이고, `제네레이터 함수`를 호출해서 반환받은 것이 `제네레이터` 이다.
- 코루틴이란 완료되지 않은 채 일시 정지했던 함수를 재개할 수 있는 기능을 가진 객체이다.
### 시작과 끝

```python
async def f():
    return 123

coro = f()
try:
    coro.send(None)
except StopIteration as e:
    print('The answer was:'. e.value)

# The answer was: 123
```
- 코루틴의 시작은 코루틴에 None을 전달하여 초기화 하는 것이다.
마지막은 StopIteration이라는 예외를 통해서 끝나게 되고, `e.value` 를 통해서 코루틴의 반환 값을 얻는다.
하지만 이와 같은 동작은 `asyncio.loop`, 즉 이벤트 루프가 내부 동작을 알아서 해주기 때문에 알 필요는 없다.

### 취소하는 법
```python
import asyncio

async def f():
    try:
        while True:
            await asyncio.sleep(0)
    except asyncio.CancelledError:
        print('취소')
    else:
        return 111

coro = f()
coro.send(None)
coro.send(None)
coro.throw(asyncio.CancelledError)
"""
    coro.throw(asyncio.CancelledError)
StopIteration
"""
```
- 위와 같이 `StopIteration`로 코루틴이 종료된다.

```python
async def c():
    await asyncio.sleep(0)
    return 111

loop = asyncio.get_event_loop()
coro = c()
print(loop.run_until_complete(coro))
### 111
```
- asyncio 사용시 내부적으로 .send(None) 호출과 StopIteration 예외를 통해서 종료되고, 값도 반환해준다.
- 여기서 await은 항상 매개변수 하나를 필요로 하는데, 허용되는 형은 `awaitable`
이어야 한다.
    - 코루틴(async def 함수의 반환값)

## 이벤트 루프
### get_event_loop()와 get_running_loop()의 차이
- `get_event_loop()`는 동일한 스레드 내에서만 동작한다. 즉, 다른 스레드에서 반환되는 loop 객체는 새로 생성된 새로운 루프 인스턴스이다.
```python
async def c():
    await asyncio.sleep(0)
    loop = asyncio.get_event_loop()
    return loop

loop = asyncio.get_event_loop()
coro = c()
print(loop is loop.run_until_complete(coro))
```
- 이 결과는 동일한 메인 스레드에서 동작하는 loop이기 때문에 같은 객체임으로 True를 반환한다.
### get_running_loop()와 get_event_loop()의 차이
```python
asycio.create_task(coro)
```
- get_event_loop()는 동일한 스레드 내에서만 동작한다.
- 반면 get_running_loop()은 코루틴, task, 혹은 함수 내에서 호출이 가능하다.
- 따라서 현재 동작중인 이벤트 루프를 반드시 얻을 수 있다.
- `asycio.create_task` 안에는 `get_running_loop()`가 내장되어있어, **loop 인스턴스를 만들지 않아도 된다.**
- 파이썬 버전업이 되면서 `get_running_loop()` 사용을 권장하고 있고, 고수준의 API는 모두 `get_running_loop()`를 사용하고 있다.
