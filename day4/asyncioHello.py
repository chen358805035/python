#异步IO
import asyncio
'''asyncio的编程模型就是一个消息循环。
我们从asyncio模块中直接获取一个EventLoop的引用，
然后把需要执行的coroutine(协程)扔到EventLoop中执行，就实现了异步IO。'''
#@asyncio.coroutine把一个generator标记为coroutine类型
@asyncio.coroutine
def hello():
	print('Heloo world!')
	#异步调用asyncio.sleep(1)
	r = yield from asyncio.sleep(1)
	print('Hello again!')

 #获取EventLoop:
loop = asyncio.get_event_loop()

 #执行coroutine
loop.run_until_complete(hello())
loop.close()