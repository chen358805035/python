#编写ORM
#ORM即Object-Relationl Mapping，它的作用是在关系型数据库和对象之间作一个映射，
#这样，我们在具体的操作数据库的时候，就不需要再去和复杂的SQL语句打交道，
#只要像平时操作对象一样操作它就可以了
import asyncio,aiomysql,logging
__autor__ = 'chen'

def log(sql, args=()):
	logging.info('SQL: %s' % sql)
#创建连接池
async def create_pool(loop, **kw):
	#**kw是一个字典
	logging.info('create database connection pool...')
	global __pool
	__pool = await aiomysql.create_pool(
		#dict提供的get()方法，如果key不存在，可以返回None，或者自己指定的value
		host = kw.get('host', 'localhost'),
		port = kw.get('port', 3306),
		user = kw['user'],
		password = kw['password'],
		db = kw['db'],
		charset = kw.get('charset', 'utf8'),#是utf8而不是utf-8
		autocommit = kw.get('autocommit', True),
		maxsize = kw.get('maxsize', 10),
		minsize = kw.get('minsize', 1),
		loop = loop
		)
#查询
async def select(sql, args, size = None):
	log(sql, args)
	global __pool#申明全局变量__pool
	#with...as 此方法主要针对于需要close的一些操作
	async with  __pool.get() as conn:
		#class DictCursor:游标将结果作为字典返回
		cur = await conn.cursor(aiomysql.DictCursor)
		print(sql.replace('?', '%s'))
		print(args)
		#replace('带操作的字符串'，'被换掉的内容'【要换的内容，可写可不写默认为null】)
		await cur.execute(sql.replace('?', '%s'), args or ())
		if size:
			#获取size数量的结果
			rs = await cur.fetchmany(size)
		else:
			#获取全部结果
			rs = await cur.fetchall()
		await cur.close()
		logging.info('rows returned:%s' % len(rs))
		return rs

#Insert（插入）, Update, Delete
async def execute(sql, args, autocommit=True):
	log(sql)
	print(sql)
	async with __pool.get() as conn:
		if not autocommit:
			await conn.begin()
		try:
			async with conn.cursor(aiomysql.DictCursor) as cur:
							
				# print(sql.replace('?', '%s'))
				# print(args)
				await cur.execute(sql.replace('?', '%s'),args)
				affected = cur.rowcount
			if not autocommit:
				await conn.commit()
			
		except BaseException as e:
			if not autocommit:
				await conn.rollback()
			# 触发异常后，后面的代码就不会再执行
			raise
		return affected

def create_args_string(num):
	L = []
	for n in range(num):
		L.append('?')
	return ', '.join(L)#return 缩进了导致出现not all arguments converted during string formatting错

class Field(object):
	def __init__(self, name, column_type, primary_key, default):
		self.name = name
		self.column_type = column_type
		self.primary_key =primary_key
		self.default = default

	def __str__(self):
		return '<%s, %s:%s>' % (self.__class__.__name__, self.column_type, self.name)

class StringField(Field):
	def __init__(self, name = None, primary_key = False, default = None, ddl = 'varchar(100)'):
		#调用父类__init__方法
		super().__init__(name, ddl, primary_key, default)

class BooleanField(Field):
	def __init__(self, name = None, default = False):
		super().__init__(name, 'boolean', False, default)

class IntegerField(Field):
	def __init__(self, name = None, primary_key = False, default = 0 ):
		super().__init__(name, 'bigint', primary_key, default)

class FloatField(Field):
	def __init__(self ,name = None, primary_key = False, default = 0.0 ):
		super().__init__(name, 'real', primary_key, default)

class TextField(Field):
	def __init__(self, name = None, default = None):
		super().__init__(name, 'text', False, default)



#通过ModelMetaclass将具体的子类的映射信息读取出来
class ModelMetaclass(type):
	def __new__(cls, name, bases, attrs):
		#排除Model类本身：
		if name == 'Model':
			return type.__new__(cls, name, bases, attrs)
		#获得table名称：
		tableName = attrs.get('__table__', None) or name
		#print(tableName)
		logging.info('found model: %s (table: %s)' % (name, tableName))
		#获取所有的Field和主键名：
		mappings = dict()
		#print(mappings)
		fields = []
		primaryKey = None
		#k==key  v==value
		for k, v in attrs.items():
			#print('k =%s , v = %s'% (k, v))

			if isinstance(v, Field):
				logging.info('	found mapping:%s ==> %s' % (k, v))
				mappings[k] = v
				if v.primary_key:
					#找到主键
					if primaryKey:
						raise RuntimeError('Duplicate primarykey for field:%s' % k )
					primaryKey = k
				else:
					fields.append(k)
		if not primaryKey:
			raise RuntimeError('Primary key not find.')
		for k in mappings.keys():
			attrs.pop(k)
		escaped_fields = list(map(lambda f: '%s' % f, fields))
		#print(escaped_fields)
		attrs['__mappings__'] = mappings#保存属性和列的映射关系
		attrs['__table__'] = tableName
		attrs['__primary_key__'] = primaryKey#主键属性名
		attrs['__fields__'] = fields#除主键值外的属性名
		# 构造默认的SELECT, INSERT, UPDATE和DELETE语句:
		#SELECT * FROM <表名> WHERE <条件表达式>
		#tableName对应数据库中表名：__table__ = 'users'、__table__ = 'blog'、__table__ = 'comment'
		#escaped_fields理解为数据库表中每一列的名称：
		#primaryKey主键：models中通过设置primary_key = True来标记主键
		attrs['__select__'] = 'select %s, %s from %s' % (primaryKey, ','.join(escaped_fields), tableName)
		attrs['__insert__'] = "insert into %s (%s, %s) value (%s)" % (tableName, ', '.join(escaped_fields), primaryKey, create_args_string(len(escaped_fields)+1)) 
		attrs['__update__'] = 'update %s set %s where %s =?' % (tableName, ','.join(map(lambda f: '"%s" =?' % (mappings.get(f).name or f), fields)), primaryKey)
		attrs['__delete__'] = 'delete from %s where %s =?' % (tableName, primaryKey)
		return type.__new__(cls, name, bases, attrs)

#定义Model
class Model(dict, metaclass = ModelMetaclass):
	def __init__(self, **kw):
		super(Model, self).__init__(**kw)
	#在访问对象的item属性的时候，如果对象并没有这个相应的属性，方法，那么将会调用这个方法来处理
	def __getattr__(self, key):
		try:
			return self[key]
		except KeyError:
			raise AttributeError(r"'Model' object has no attribute '%s'" % key)
	#当试图对对象的item特性赋值的时候将会被调用。
	def __setattr__(self, key, value):
		self[key] = value

	def getValue(self, key):
		return getattr(self, key, None)

	def getValueOrDefault(self, key):
		value = getattr(self, key, None)
		#print(value)
		if value is None:
			field = self.__mappings__[key]
			if field.default is not None:
				value = field.default() if callable(field.default) else field.default
				logging.debug('using default value for %s: %s' % (key, str(value)))
				setattr(self, key, value)
		return value
	@classmethod
	async def findAll(cls, where = None, args = None, **kw):
		'find objectby where clause.'
		sql= [cls.__select__]
		if where:
			sql.append('where')
			sql.append(where)
		if args is None:
			args = []
		orderBy = kw.get('orderBy', None)
		if orderBy:
			sql.append('order by')
			sql.append(orderBy)
		limit = kw.get('limit', None)
		if limit is not None:
			sql.append('limit')
			if isinstance(limit, int):
				sql.append('?')
				args.apppend(limit)
			elif isinstance(limit, tuple) and len(limit) == 2:
				sql.append('?, ?')
				args.extend(limit)
			else:
				raise ValueError('Invalid limit value: %s' % str(limit))
		rs = await select (' '.join(sql), args)
		return [cls(**r) for r in rs]

	@classmethod
	async def findNumber(cls, selectField, where = None, args = None):
		'find number by select and where.'
		sql = ['select %s _num_ from %s' % (selectField, cls.__table__)]
		if where:
			sql.append('where')
			sql.append(where)
		# print(sql)
		# print(args)
		# print(' '.join(sql))
		rs = await select(' '.join(sql), args, 1)
		if len(rs) == 0:
			return None
		return rs[0]['_num_']

	#按主键值查询
	@classmethod
	async def find(cls, pk):
		'find object by primary key'

		rs = await select('%s where %s =?' % (cls.__select__, cls.__primary_key__), [pk], 1)
		if len(rs) == 0:
			return None
		return cls(**rs[0])

	async def save(self):
		args = list(map(self.getValueOrDefault, self.__fields__))
		args.append(self.getValueOrDefault(self.__primary_key__))
		#print(args)
		row = await execute(self.__insert__, args)
		if row != 1:
			logging.warn('faild to insert record: affected rows: %s' % rows)

	async def update(self):
		args = list(map(self.getValue, self.__fields__))
		args.append(self.getValue(self.__primary_key__))
		rows = await execute(self.__update__, args)
		if rows != 1:
			logging.warn('faied to updata by primary key: affected rows: %s' % rows)

	async def remove(self):
		args = [self.getValue(self.__primary_key__)]
		rows = await execute(self.__delete__, args)
		if rows != 1:
			logging.warn('faied to remove by primary key : affected rows: %s' % rows)





