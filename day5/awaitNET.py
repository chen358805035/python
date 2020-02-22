import asyncio

async def wget(host):
	print('wget %s...' % host)
	connect = asyncio.open_connection(host, 80)
	reader, writer = await  connect
	header = 'GET / HTTP/1.0\r\nHost: %s\r\n\r\n' % host
	writer.write(header.encode('utf-8'))
	await writer.drain()
	while True:
		line = await reader.readline()
		if line == b'\r\n':
			break
		#rstrip() 删除 string 字符串末尾的指定字符（默认为空格）.
		print('%s header > %s' % (host, line.decode('utf-8').rstrip()))
	writer.close()

loop = asyncio.get_event_loop()
tasks = [wget(host) for host in [ 'www.baidu.com', 'www.sohu.com', 'www.sina.com.cn']]
loop.run_until_complete(asyncio.wait(tasks))
loop.close()