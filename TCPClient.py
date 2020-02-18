#导入socket库
#新浪强制HTTPS协议 所以80端口改443；socket改 ssl
import socket
import ssl
#创建一个socket: AF_INET指定IPV4协议； 
#SOCK_STREAM指定使用面向流的TCP协议
s = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
#s = ssl.wrap_socket(socket.socket())

#建立连接：  参数是tuple(元组)
s.connect(('www.baidu.com', 80))
#s.connect(('www.sina.com.cn', 443))

#发送数据：
#s.send(b'GET / HTTP/1.1\r\nHost: www.sina.com.cn\r\nConnection: close\r\n\r\n')
s.send(b'GET / HTTP/1.1\r\nHost: www.baidu.com\r\nConnection: close\r\n\r\n')

#接收数据： 调用recv(max)方法，一次最多接收指定的字节数
buffer = []
while True:
	#每次最多接受1K字节：
	d = s.recv(1024)
	if d:
		#如果d不为空，把接收的数据以循环拼接的方式存入buffer中
		buffer.append(d)
	else:
		break
print(buffer,'\r\n')

#b'' 是一个空字节 join 连接字符串；
#使用空字节把buffer这个字节列表连接在一起，成为一个新的字节串
data = b''.join(buffer)
print(data)
#关闭连接
s.close()

#以'\r\n\r\n'为分隔符分割成两部分，分别给header和html变量
header, html = data.split(b'\r\n\r\n', 1)
print(header.decode('utf-8'))
#把接收的数据写入文件：
with open('C:/Users/Administrator/Desktop/baidu.html', 'wb') as f:
	f.write(html)
