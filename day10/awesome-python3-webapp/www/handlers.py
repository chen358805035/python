'url handlers'

import re, time, json, logging, hashlib, base64, asyncio
from coroweb import get, post
from models import User, Comment, Blog, next_id
from apis import APIValueError, APIResourceNotFoundError, APIError
from config import configs
from aiohttp import web

COOKIE_NAME = 'awesession'
_COOKIE_KEY = configs.session.secret

#计算加密cookie
def user2cookie(user, max_age):
	'''
	Generate cookie str by user
	'''
	#build cookie string by:id-expires-sha1
	expires = str(int(time.time() + max_age))
	s = '%s-%s-%s-%s' % (user.id, user.passwd, expires, _COOKIE_KEY)
	L = [user.id, expires, hashlib.sha1(s.encode('utf-8')).hexdigest()]
	return '-'.join(L)

async def cookie2user(cookie_str):
	'''
	Parse cookie and load user if cookie is valid
	'''
	if not cookie_str:
		return None
	try:
		L = cookie_str.split('-')
		if len(L) != 3:
			return None
		uid, expires, sha1 = L
		if int(expires) < time.time():
			return None
		user = await User.find(uid)
		if user is None:
			return None
		#SHA1("用户id" + "用户口令" + "过期时间" + "SecretKey")
		s = '%s-%s-%s-%s' % (uid, user.passwd, expires, _COOKIE_KEY)
		if sha1 != hashlib.sha1(s.encode('utf-8')).hexdigest():
			logging.info('invalid sha1')
			return None
		user.passwd = '******'
		return user
	except Exception as  e:
		logging.exception(e)
		return None


#处理首页URL的函数：

@get('/')
async def index(request):
	summary = 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.'
	blogs = [
		Blog(id = '1', name = 'Test Blog', summary = summary, created_at = time.time()-120),
		Blog(id = '2', name = 'Something New', summary = summary, created_at = time.time()-3600),
		Blog(id = '3', name ='Learn Swift', summary = summary, created_at = time.time()-7200)
	]

	return { '__template__' : 'blogs.html', 'blogs' : blogs}

@get('/register')
def register():
	return {'__template__' : 'register.html'}

@get('/signin')
def signin():
	return {'__template__' : 'signin.html'}

@post('/api/authenticate')#POST请求写成了GET,浏览器出现405错误
async def authenticate(*, email, passwd):
	if not email:
		raise APIValueError('email', 'Invalid email.')
	if not passwd:
		raise APIValueError('passwd', 'Invalid passwd.')
	users = await User.findAll('email = ?', [email])
	if len(users) == 0:
		raise APIValueError('email ', 'Email not exist')
	user = users[0]
	#核对密码
	sha1 = hashlib.sha1()
	sha1.update(user.id.encode('utf-8'))
	sha1.update(b':')
	sha1.update(passwd.encode('utf-8'))
	if user.passwd != sha1.hexdigest():
		raise APIValueError('passwd', 'Invaild passwrod.')
	#核对成功，设置cookie:
	r = web.Response()
	r.set_cookie(COOKIE_NAME, user2cookie(user, 86400), max_age = 86400, httponly = True)
	user.passwd = '******'
	r.content_type = 'application/json'
	r.body = json.dumps(user, ensure_ascii = False).encode('utf-8')
	return r

@get('/signout')
def signout(request):
	referer = request.headers.get('Referer')
	r = web.HTTPFound(referer or '/')
	r.set_cookie(COOKIE_NAME, '-deleted-', max_age = 0, httponly = True)
	logging.info('user signed out.')
	return r

_RE_EMAIL = re.compile(r'^[a-z0-9\.\-\_]+@[a-z0-9\-\_]+(\.[a-z0-9\-\_]+){1,4}$')
_RE_SHA1 = re.compile(r'^[0-9a-f]{40}$')

@post('/api/users')
async def api_register_user(*, email, name, passwd):
	if not name or not name.strip():
		raise APIValueError('name')
	if not email or not _RE_EMAIL.match(email):
		raise APIValueError('email')
	if not passwd or not _RE_SHA1.match(passwd):
		raise APIValueError('passwd')
	users = await User.findAll('email = ?', [email])
	if len(users) > 0:
		raise APIError('register:failed', 'email', 'Email is already in use.')
	uid = next_id()
	sha1_passwd = '%s:%s' % (uid, passwd)
	user = User(id = uid, name = name.strip(), email = email, passwd = hashlib.sha1(sha1_passwd.encode('utf-8')).hexdigest(), image = 'http://www.gravatar.com/avatar/%s?d=mm&s=120' % hashlib.md5(email.encode('utf-8')).hexdigest())
	await user.save()
	#制作会话cookie:
	r = web.Response()
	r.set_cookie(COOKIE_NAME, user2cookie(user, 86400), max_age = 86400, httponly = True)
	user.passwd = '******'
	r.content_type = 'application/json'
	r.body = json.dumps(user, ensure_ascii = False).encode('utf-8')
	logging.info('body = %s', r.body)
	return r
def text2html(text):

	lines = map(lambda s: '<p>%s</p>' % s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'), filter(lambda s: s.strip() != '', text.split('\n')))
	return ''.join(lines)
# #创建Blog
@get('api/blogs/{id}')
async def api_get_blog(*, id):
	blog = await Blog.find(id)
	return blog

@post('/api/blogs')
async def api_create_blog(request, *, name, summary, content):
	check_admin(request)
	if not name or not name.strip():
		raise APIValueError('name', 'name cannot be empty.')
	if not summar or not summary.strip():
		raise APIValueError('summary', 'summary cannot be empty.')
	if not content or not content.strip():
		raise APIValueError('content', 'content cannot be empty.')
	blog = Blog(user_id = request.__user__.id, user_name = request.__user__.name, user_image = request.__user__.image, name = name.strip(), summary = summary.strip(), content = content.strip())
	await blog.save()
	return blog

@get('/blog/{id}')
def get_blog(id):
	blog = yield from Blog.find(id)
	comments = yield from Comment.findAll('blog_id=?', [id], orderBy='created_at desc')
	for c in comments:
		c.html_content = text2html(c.content)
	blog.html_content = markdown2.markdown(blog.content)
	return {
		'__template__': 'blog.html',
		'blog': blog,
		'comments': comments
	}

