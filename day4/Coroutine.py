#带有 yield 的函数不再是一个普通函数，而是一个生成器generator，可用于迭代
def consumer():
	r = ''
	while True:
		n = yield r
		if not n:
			return
		print('[CONSUMER] Consuming %s...' % n)
		r = '200 OK'

def produce(c):
	#next()等同于send(None)
	#第一次调用时必须先next()或send(None)，否则会报错，
	#send后之所以为None是因为这时候没有上一个yield
	c.send(None)
	n = 0
	while n < 5:
		n += 1
		print('[PRODUCER Producing %s...' %n)
		r = c.send(n)#send可以强行修改上一个yield表达式值
		#打印yield的返回值
		print('[PRODUCER Consuming return: %s' % r)
	c.close()

c = consumer()
produce(c)