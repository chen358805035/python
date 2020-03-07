from flask import Flask ,redirect, url_for, request

app  = Flask(__name__)
#GET以未加密的形式将数据发送到服务器。最常见的方法
#HEAD和GET方法相同，但没有响应体。
#POST 用于将HTML表单数据发送到服务器。POST方法接收的数据不由服务器缓存。
#PUT 用上传的内容替换目标资源的所有当前表示。
#DELETE 删除由URL给出的目标资源的所有当前表示。
@app.route('/success/<name>')
def success(name):
	return 'welcome %s' % name

@app.route('/login', methods = ['POST', 'GET'])
def login():
	if request.method == 'POST':
		user = request.form['nm']
		return redirect(url_for('success', name = user))
	else:
		user = request.args.get('nm')
		return redirect(url_for('success', name = user))

app.run(debug = True)