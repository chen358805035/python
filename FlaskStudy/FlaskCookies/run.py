from flask import Flask , render_template, request,make_response

app = Flask(__name__)
#Cookie以文本文件的形式存储在客户端的计算机上。
#其目的是记住和跟踪与客户使用相关的数据，以获得更好的访问者体验和网站统计信息。

#Request对象包含Cookie的属性。
#它是所有cookie变量及其对应值的字典对象，客户端已传输。
#除此之外，cookie还存储其网站的到期时间，路径和域名。

#在Flask中，对响应对象设置cookie。
#使用make_response()函数从视图函数的返回值获取响应对象。
#之后，使用响应对象的set_cookie()函数来存储cookie。
@app.route('/')
def index():
	return render_template('index.html')


@app.route('/setcookie', methods = ['POST', 'GET'])
def setcookie():
	if request.method == 'POST':
		user = request.form['name']

	# resp = make_response(render_template('index.html'))
	# resp.set_cookie('userID', user)

	return '%s' % request.form

@app.route('/getcookie')
def getcookie():
	name = request.cookies.get('userID')
	return '<h1> Welcome %s </h1>' % name

app.run(debug =True)