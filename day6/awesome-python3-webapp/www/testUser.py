import asyncio,orm
from models import User, Blog, Comment

async def test(loop):
	await orm.create_pool( user = 'www-data', password = 'www-data', db = 'awesome', loop = loop)
	#插入
	# u = User ( id = '1' , name = '_num_Test', email = 'test1@example.com', passwd = '123456', image = 'about:blank')
	# await u.save()


	#查询全部
	#u = User(id ='1')
	# users = await u.findAll()
	# print(users)
	#按主键值查询
	u = User(id ='1')
	users = await u.find( pk = 1)
	print(users)
	
	#删除
	# u = User (id = '1')
	# await u.remove()

#test()

loop = asyncio.get_event_loop()
loop.run_until_complete(test(loop))
loop.close()
