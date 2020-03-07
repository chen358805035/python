from flask import Flask 

app = Flask(__name__)
#通过向规则参数添加变量部分，可以动态构建URL。
#此变量部分标记为<variable-name>。它作为关键字参数传递给与规则相关联的函数。
@app.route('/')
def hello_world():
	return 'hello world'

@app.route('/<name>')
def hello(name):
	
	return 'hello %s!' % name
	

@app.route('/blog/<int:ID>')
def blog(ID):
	return 'blog number %d' % ID

@app.route('/value/<float:V>')
def value(V):
	return 'value = %f' % V

app.run(debug = True) 