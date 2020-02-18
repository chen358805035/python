import socket 

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect(('127.0.0.1', 8888))

print(s.recv(1024).decode('utf-8'))
for data in [b'chen',b'xiao']:
	s.send(data)
	print(s.recv(1024).decode('utf-8'))

s.send(b'exit')
s.close()