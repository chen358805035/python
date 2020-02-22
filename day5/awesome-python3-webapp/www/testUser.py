from orm import Model, StringField, IntegerField

import asyncio,orm
class User(Model):
	__table__ = 'users'

	id = IntegerField(primary_key = True)
	name = StringField()

async def test(loop):
	await orm.create_pool(loop =loop, user = 'root', password = '', db = 'awesome')
	user = User (id = 111, name = 'chen')
	await user.save()

	# users= User.findAll()
	# print(users)

#test()

loop = asyncio.get_event_loop()
loop.run_until_complete(test(loop))
loop.run_forever()
# #创建实例
# user  = User(id = 123, name = 'Michael')
# #存入数据库
# #user.save()
# #查询所有User对象
# users = User.findAll()

# print(users)