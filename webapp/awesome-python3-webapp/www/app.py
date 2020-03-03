#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#WEB APP骨架
import logging; logging.basicConfig(level = logging.INFO)

import asyncio, os, json, time
from datetime import datetime
from aiohttp import web
from config import configs
import orm
from jinja2 import Environment, FileSystemLoader
from coroweb import add_routes, add_static
from handlers import cookie2user, COOKIE_NAME
#jinja2模块自注册
def init_jinja2(app, **kw):
	logging.info('init jinja2...')
	options = dict(
		autoescape = kw.get('autoescape', True),
		block_start_string = kw.get('block_start_string', '{%'),
		block_end_string = kw.get('block_end_string', '%}'),
		variable_start_string = kw.get('variable_start_string', '{{'),
		variable_end_string = kw.get('variable_end_string','}}'),
		auto_reload = kw.get('auto_reload', True)
		)
	path = kw.get('path', None)
	if path is None:
		path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
	logging.info('set jinja2 templates path:%s ' % path)
	env = Environment(loader = FileSystemLoader(path), **options)
	filters = kw.get('filters', None)
	logging.info('jinja2  init templates %s' % filters)
	if filters is not None:
		for name, f in filters.items():
			logging.info('filter name %s ...%s' % (name, f) )
			env.filters[name] = f
	app['__templating__'] = env

#middleware是一种拦截器,可以改变URL的输入、输出，甚至可以决定不继续处理而直接返回
async def logger_factory(app, handler):
	async def logger(request):
		logging.info('Request:%s %s' % (request.method, request.path))
		return (await handler(request))
	return logger#写掉return 出现了'NoneType' object is not callable错误 弄了半天
#利用middle在处理URL之前，把cookie解析出来，并将登录用户绑定到request对象上，
#这样，后续的URL处理函数就可以直接拿到登录用户
async def auth_factory(app, handler):
	async def auth(request):
		logging.info('check users:%s %s' % (request.method, request.path))
		request.__user__ = None
		cookie_str = request.cookies.get(COOKIE_NAME)
		if cookie_str:
			user = await cookie2user(cookie_str)
			if user:
				logging.info('set current user: %s' % user.email)
				request.__user__ = user
		if request.path.startswith('/mange/') and (request.__user__ is None or not request.__uesr__.admin):
			return web.HTTPFound('/signin')
		return (await handler(request))
	return auth

async def data_factory(app, handler):
	async def parse_data(request):
		if request.method == 'POST':
			if request.content_type.startswith('application/json'):
				request.__data__ = await request.json()
				logging.info('request json: %s' % str(request.__data__))
			elif request.content_type.startswith('application/x-www-form-urlencoded'):
				request.__data__ = await request.post()
				logging.info('request form: %s' % str(request.__data__))
		return (await handler(request))
	return parse_data

async def response_factory(app, handler):
	async def response(request):
		logging.info('Response handler...')
		#handler(request)是一个协程函数，是处理web-handler过程的抽象函数，web-handler是指返回http的相应的端点
		r = await handler(request)
		if isinstance(r, web.StreamResponse):
			return r
		if isinstance(r, bytes):
			resp = web.Response(body = r)
			resp.content_type = 'application/octet-stream'
			return resp
		if isinstance(r, str):
			if r.startswith('redirect:'):
				return web.HTTPFound(r[9:])
			resp = web.Response(body = r.encode('utf-8'))
			resp.content_type = 'text/html; charset = utf-8'
			return resp
		if isinstance(r, dict):
			template = r.get('__template__')
			if template is None:
				resp = web.Response(body = json.dumps(r, ensure_ascii = False, default = lambda o: o.__dict__).encode('utf-8'))
				resp.content_type = 'application/json; charset=utf-8'
				return resp
			else:
				r['__user__'] = request.__user__
				resp = web.Response(body = app['__templating__'].get_template(template).render(**r).encode('utf-8'))
				logging.info('resp %s' % resp)
				resp.content_type = 'text/html; charset = utf-8'
				return resp
		if isinstance(r, int) and r>=100 and r<600:
			return web.Response(r)
		if isinstance(r, tuple) and len(r) == 2:
			t, m = r
			if isinstance(t, int) and t>=100 and t<600:
				return web.Response(t, str(m))
		resp = web.Response(body = str(r).encode('utf-8'))
		resp.content_type = 'text/plain;charset = utf-8'
		return resp
	return response

#jinja2的filter（过滤器），把一个浮点数转换成日期字符串。
# @app.template_filter('datetime')
def datetime_filter(t):
	delta = int(time.time() - t)
	if delta < 60:
		return u'1分钟前'
	if delta < 3600:
		return u'%s分钟前' % (delta // 60)
	if delta < 86400:
		return u'%s小时前' % (delta // 3600)
	if delta < 604800:
		return u'%s天前' % (delta // 86400)
	dt = datetime.fromtimestamp(t)
	return u'%s 年 %s 月 %s 日' % (dt.year, dt.month, dt.day)

# def index(request):
# 	return web.Response(body = b'<h1>DiDiao</h1>', content_type = 'text/html')

async def init(loop):
	await orm.create_pool(loop = loop, **configs.db)
	app = web.Application(loop = loop, middlewares = [auth_factory, logger_factory, response_factory])
	init_jinja2(app, filters = dict(datetime = datetime_filter))

	add_routes(app, 'handlers')
	add_static(app)
	srv = await loop.create_server(app.make_handler(), '127.0.0.1', 9002)
	logging.info('server started at http://127.0.0.1:9000...')
	return srv
	# app = web.Application(loop = loop)
	# app.router.add_route('GET', '/', index)
	# srv = await loop.create_server(app.make_handler(), '127.0.0.1', 9001)
	# logging.info('server started at http://127.0.0.1:9000...')
	# return srv

loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop))
loop.run_forever()
