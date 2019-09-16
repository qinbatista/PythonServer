'''
config_reader.py
'''

import time
import requests
import configparser

CM = 'http://localhost:8000/get_server_config_location'

def wait_config():
	'''
	Fetches the server configuration file from the location specified by the configuration manager.
	'''
	print(f'Reading configuration file from config_manager at {CM}...')
	while True:
		try:
			r = requests.get(CM)
			parser = configparser.ConfigParser()
			parser.read(r.json()['file'])
			print('done.')
			return parser
		except requests.exceptions.ConnectionError:
			print('Could not find configuration server, retrying in 5 seconds...')
			time.sleep(5)
