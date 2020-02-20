#从wsgiref模块导入
from wsgiref.simple_server import make_server
#导入编写的application函数
#from hello import application

def application(environ, start_response):
	start_response('200 OK', [('Connect-Type', 'text/html')])
	body = '<h1>Hello, %s!</h1>' % (environ['PATH_INFO'][1:] or 'web')
	return [body.encode('utf-8')]
    
#创建一个服务器，ip为空，端口为8000，处理函数是application
httpd = make_server('',8000, application)
print('Serving HTTP on port 8000...')

#开启监听HTTP请求：
httpd.serve_forever()
