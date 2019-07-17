import requests

PLAYER_BASE_URL = "http://localhost:9999"


def test_try_remove_coin():
	result = requests.post(PLAYER_BASE_URL + '/try_remove_coin', data={'unique_id': "4", "value": 255})
	print(str(result.text))
	
	
def test_try_remove_iron():
	result = requests.post(PLAYER_BASE_URL + '/try_remove_iron', data={'unique_id': "4", "value": -50})
	print(str(result.text))
	
	
def test_try_remove_diamond():
	result = requests.post(PLAYER_BASE_URL + '/try_remove_diamond', data={'unique_id': "4", "value": -1000})
	print(str(result.text))
	

if __name__ == "__main__":
	# test_try_remove_coin()
	test_try_remove_iron()
	# test_try_remove_diamond()