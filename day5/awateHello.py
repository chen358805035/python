import asyncio, threading

#async和await是针对coroutine的新语法，要使用新的语法，只需要做两步简单的替换：

#1、把@asyncio.coroutine替换为async；
#2、把yield from替换为await。

async def hello():
	print('Hello world! %s' % threading.currentThread())
	await asyncio.sleep(1)
	print('Hello again! (%s)' % threading.currentThread())

loop = asyncio.get_event_loop()
tasks = [hello(), hello()]
loop.run_until_complete(asyncio.wait(tasks))
loop.close()