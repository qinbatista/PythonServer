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
				msg_list.insert(tkinter.END, f'<{command}> ' + payload)
				msg_list.see('end')
			else:
				BUFFER += client_socket.recv(MAXSIZE)
		except OSError:  # Possibly client has left the chat.
			break
	msg_list.insert(tkinter.END, 'Disconnected from server...')


def spam():  # event is passed by binders.
	"""Handles sending of messages."""
	while True:
		try:
			client_socket.sendall(make_message('PUBLIC', ''.join([random.choice(string.ascii_letters + string.digits) for n in range(random.randint(1, 100))])))
			time.sleep(random.random() * 1)
		except OSError:
			break


def on_closing(event=None):
	"""This function is to be called when the window is closed."""
	client_socket.sendall(make_message('EXIT'))
	client_socket.close()
	top.quit()

top = tkinter.Tk()
top.title("Chatter")

messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()  # For the messages to be sent.
my_msg.set('')
scrollbar = tkinter.Scrollbar(messages_frame)  # To navigate through past messages.
# Following will contain the messages.
msg_list = tkinter.Listbox(messages_frame, height=15, width=100, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()


top.protocol("WM_DELETE_WINDOW", on_closing)

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

name = f'chatter{sys.argv[1]}'
top.title(name)

client_socket.sendall(make_message('REGISTER', name))


receive_thread = Thread(target=receive, daemon = True)
receive_thread.start()

spam_thread = Thread(target = spam, daemon = True)
spam_thread.start()

tkinter.mainloop()	# Starts GUI execution.
