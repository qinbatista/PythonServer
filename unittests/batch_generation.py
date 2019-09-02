import tormysql
import asyncio

pool = tormysql.ConnectionPool(max_connections=10, host='127.0.0.1', user='root', passwd='lukseun', db='aliya', charset='utf8')

def user_generation(unique_id: str):
	pass


def account_generation(unique_id: str):
	pass


def email_generation(unique_id: str):
	pass


def phone_generation(unique_id: str):
	pass


async def generation(unique_id: str, conn: tormysql):
	cursor = conn.cursor()
	await cursor.execute(f"select * from player where unique_id='{unique_id}'")
	data = cursor.fetchall()
	print(f"data:{data}")


async def run():
	unique_id = input("请输入要批量生成的unique_id：")
	await generation(unique_id, await pool.Connection())
	pool.closed()


if __name__ == '__main__':
	asyncio.run(run())
