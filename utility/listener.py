#!/usr/bin/env python3
"""Script for Tkinter GUI chat client."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import sys
import tkinter
import requests
import configparser
import time
import random
import string

MAXSIZE = 4096
BUFFER = b''

def make_message(command, message = ''):
	return (command.zfill(10) + message + '\r\n').encode()

def receive():
	"""Handles receiving of messages."""
	global BUFFER
	while True:
		try:
			if b'\r\n' in BUFFER:
				msg, BUFFER = BUFFER.split(b'\r\n', maxsplit = 1)
				msg = msg.decode('utf8')
				if msg == '' or msg == None:
					break
				command, payload = msg[:10].lstrip('0'), msg[10:]
				print(f'<{command}> {payload}')
			else:
				BUFFER += client_socket.recv(MAXSIZE)
		except OSError:  # Possibly client has left the chat.
			break


def on_closing(event=None):
	"""This function is to be called when the window is closed."""
	client_socket.sendall(make_message('EXIT'))
	client_socket.close()

#----Now comes the sockets part----
HOST = '127.0.0.1'
#HOST = 'remote4.magicwandai.com'
PORT = 8300

ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

if len(sys.argv) != 2:
	print('missing required argument: chatter number')
	sys.exit(-1)

name = f'listener{sys.argv[1]}'

client_socket.sendall(make_message('REGISTER', name))


receive_thread = Thread(target=receive, daemon = True)
receive_thread.start()

while True:
	time.sleep(5)
