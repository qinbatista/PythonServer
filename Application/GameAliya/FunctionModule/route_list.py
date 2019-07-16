@ROUTES.post('/decrease_energy')
async def __decrease_energy(request: web.Request) -> web.Response:
	post = await request.post()
	data = await MANAGER.decrease_energy(post['unique_id'], post['weapon'])
	return _json_response(data)

@ROUTES.post('/increase_energy')
async def __increase_energy(request: web.Request) -> web.Response:
	post = await request.post()
	data = await MANAGER.increase_energy(post['unique_id'], post['weapon'])
	return _json_response(data)

@ROUTES.post('/get_all_supplies')
async def __get_all_supplies(request: web.Request) -> web.Response:
	post = await request.post()
	data = await MANAGER.get_all_supplies(post['unique_id'], post['weapon'], int(post['iron']))
	return _json_response(data)

@ROUTES.post('/increase_supplies')
async def __increase_supplies(request: web.Request) -> web.Response:
	post = await request.post()
	data = await MANAGER.increase_supplies(post['unique_id'], post['weapon'], post['passive'])
	return _json_response(data)

@ROUTES.post('/random_gift_segment')
async def __random_gift_segment(request: web.Request) -> web.Response:
	post = await request.post()
	data = await MANAGER.random_gift_segment(post['unique_id'], post['weapon'])
	return _json_response(data)

@ROUTES.post('/level_up_scroll')
async def __level_up_scroll(request: web.Request) -> web.Response:
	post = await request.post()
	data = await MANAGER.level_up_scroll(post['unique_id'], post['scroll_id'])
	return _json_response(data)
