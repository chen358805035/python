from flask import Flask
from flask import request
# 声明一个Flask的类，__name__参数的作用是为了确定程序的根目录，以便获得静态文件的模板文件
app = Flask(__name__)

# @app.router()是一个装饰器，它的作用就是把视图函数(可以简单的理解成就是它下面的函数)
#与某一个url(后面括号中的部分)绑定,当访问这个url时，就会运行这个视图函数
# methods指定请求这个url的方法，默认是get，这里指定使用get或post两种方式
@app.route('/', methods = ['GET', 'POST'])
def home():
	return '<h1>Home</h1>'

@app.route('/signin', methods = ['GET'])
def signin_from():
	return '''<form action = "/signin" method = "post">
			<p><input name="usernam"></p>
			<p><input name="password"></p>
			<p><button type="submit">Sign In</button></p>
			</form>'''

@app.route('/signin', methods = ['POST'])
def signin():
	#需要从request对象读取表单内容
	if request.form['username']=='chen' and request.form['password']=='password':
		return '<h3>Hello,chen!</h3>'
	return '<h3>Bad username or password</h3>'

if __name__ == '__main__':
	app.run()