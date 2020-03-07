from flask import Flask


app = Flask(__name__)
#@app.route装饰器和app.add_url_rule方法效果一样
# @app.route('/hello')
# def hello():
# 	return 'hello world'
def hello():
	return 'hello world'
app.add_url_rule('/', '', hello)

app.run(debug = True)