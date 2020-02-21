from flask import Flask, request, render_template

# 声明一个Flask的类，__name__参数的作用是为了确定程序的根目录，以便获得静态文件的模板文件
app =Flask(__name__)
#@app.route把它下面的视图函数与括号中的url绑定；当访问这个url时，就执行这个视图函数。
@app.route('/', methods = ['GET','POST'])
def home():
	# render_template对页面进行渲染，如果页面中存在待接受的参数，可将参数放在后面
	return render_template('home.html')

@app.route('/signin', methods = ['GET'])
def signin_form():
	return render_template('form.html')

@app.route('/signin', methods = ['POST'])
def signin():
	username = request.form['username']
	password = request.form['password']
	if username=='chen' and password=='123':
		return render_template('signin-ok.html', username=username)#传入username参数
	return render_template('form.html', message='Bad username or password', username=username)

if __name__ =='__main__':
	app.run()