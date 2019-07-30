# How to add code to server system
#如何向server system添加代码

Adding code to server system should be a very simple task if you have a good understanding about how the systems work together. If you are not sure, ask Matthew.
给serever system添加代码是非常容易带事情，如果有谁吗不确定，问一下马修

## Step 1) Identify which function you want to add to the server.
## 第一步，定义你想给服务器加入方法
Look at the existing function list, and confirm that the function you need is not already there. We don't want to add duplicate functions, which will clutter the API. Make sure that the public API can't be abused by the client side. For example, don't create an API that runs an SQL request directly from the JSON - that would be very bad.


## Step 2) Once you know which function you want to add, determine which Manager it belongs to.

There are several Manager classes already. Chances are that the function you want to add, should belong to one of the existing Manager classes. For example, if you want to add a function that works with Weapons, that should be part of the WeaponManager class. Don't create a new Manager unless it is really needed.


## NOTE: This example will create a new public function relating to weapons. We will choose to create a new function called 'get\_weapon\_star' which will return the level of the weapon star specified by the client.


## Step 3) Modify the Manager code.

This is where you start to write new code. Open the correct Manager class, and first define a public method inside the class called get\_weapon\_star. Make sure the function is async. Think about what arguments you would need in order to find such data. Minimally, we would need to know the user's unique\_id as well as the weapon they are talking about. So, add those two things as arguments to your new function. This function should return a dictionary.

```python
async def get_weapon_star(self, unique_id: str, weapon: str) -> dict:
	pass
```


Now, we can put our function logic here.  Typically, we will want to define 'helper' functions to interface with the database. Here is a helper function:

```python
async def _get_weapon_star(self, unique_id: str, weapon: str) -> int:
	data = await self._execute_statement("SELECT `" + str(weapon) + "` FROM weapon_bag WHERE unique_id='" + str(unique_id) + "';")
	if () in data or data == None:
		return 0
	return data[0][0]
```

So, our main function logic becomes very simple:

```python
async def get_weapon_star(self, unique_id: str, weapon: str) -> dict:
	data = await self._get_weapon_star(unique_id, weapon)
	return {'status' : 0, 'message' : 'success', 'data' : {'star_level' : data}}
```

NOTE: JSON request format errors, and invalid token errors are handled in another location automatically, so you don't need to worry about those.


## Step 4) Add the the HTTP listener to that function.

Navigate to the bottom of the Manager file. You will find code that looks like this:

```python
@ROUTES.post('/level_up_weapon')
async def __level_up_weapon(request: web.Request) -> web.Response:
    post = await request.post()
    data = await MANAGER.level_up_weapon(post['unique_id'], post['weapon'], post['iron'])
    return _json_response(data)
```

It is very simple to add an HTTP listener for the function you just built:

```python
@ROUTES.post('/get_weapon_star')
async def __get_weapon_star(request: web.Request) -> web.Response:
    post = await request.post()
    data = await MANAGER.get_weapon_star(post['unique_id'], post['weapon'])
    return _json_response(data)
```

You create a new async function with (request) as the only parameter. You then add the function decorator @ROUTES.post('/get\_weapon\_star'). This decorator is what tells the HTTP server to listen for POST requests on the address '/get\_weapon\_star'. The POST data should be the same data as the arguments for your function. In our case, our function only needs unique\_id and weapon, so we only get those two values from the POST request.



At this point, you are done modifying the WeaponManager file. Next, we need to add our new function to our MessageResolver.


## Step 5) Add new function to message resolver

Open the MessageResolver class.

Create a new async function in the MessageHandler class called \_get\_weapon\_star. The arguments to the function are always the same.

```python
async def _get_weapon_star(self, message: dict, session) -> str:
	async with session.post(WEAPON_MANAGER_BASE_URL + '/get_weapon_star', data = {'unique_id' : message['data']['unique_id'], 'weapon' : message['data']['weapon']}) as resp:
	return await resp.text()
```

Notice a few things:

- The URL we use is WEAPON\_MANAGER\_BASE\_URL + '/get\_weapon\_star'. This makes it easy to change the WeaponManager url.
- The data parameter to the session.post() function is the JSON data we want to send to our weapon manager. Remember, we want to send the same data to our WeaponManager: unique\_id and weapon.
- If one of the arguments does not exist in the message dict, a KeyError will be raised and caught in the calling function, returning an error message to the client.



Finally, you need to add your new function to the FUNCTION\_LIST, so that the MessageResolver knows which function to call.

```python
FUNCTION_LIST = {
				......
				'get_weapon_star' : MessageHandler._get_weapon_star
				}
```

By default, all functions required a valid token to be present. If your function does not require a valid token, you can add your function name to the DOES\_NOT\_NEED\_TOKEN set.

```python
DOES_NOT_NEED_TOKEN = {'get_weapon_star'}
```



## Congratulations, you should have successfully added a function to our server system.








