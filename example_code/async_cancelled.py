import asyncio

# async def f():
#     try:
#         while True:
#             await asyncio.sleep(0)
#     except asyncio.CancelledError:
#         print('취소')
#     else:
#         return 111
    
# coro = f()
# coro.send(None)
# coro.send(None)
# coro.throw(asyncio.CancelledError)

async def c():
    await asyncio.sleep(0)
    loop = asyncio.get_event_loop()
    return 111

loop = asyncio.get_event_loop()
coro = c()
print(loop.run_until_complete(coro))