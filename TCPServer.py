import socket
import threading,time

def server():
	#创建scoket:
	s =socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	#监听端口：
	s.bind(('127.0.0.1',8888))

	#调用listen()方法开始监听端口,传入的参数指定等待连接的最大数量
	s.listen(5)
	print('Waiting for connection...')


	while True:
		#接收一个新连接：
		sock, addr = s.accept()
		#创建新线程来处理TCP连接：
		t = threading.Thread(target=tcplink, args=(sock, addr))
		t.start
		print('threading start')
		print(sock,addr)


def tcplink(sock, addr):

	print('Accept new connection from %s:%s...' % addr)
	sock.send(b'Wlcome!')
	while True:
		data = sock.recv(1024)
		time.sleep(1)
		#如果数据为空或者接收到exit就退出
		if not data or data.decode('utf-8') =='exit':
			break
		sock.send(('Hello,%s!' % data.decode('utf-8')).encode('utf-8'))
	sock.close()
	print('Connection from %s:%s closed.' % addr)

if __name__ == '__main__':
	server()