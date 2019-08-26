#!/usr/bin/env python3
"""Script for Tkinter GUI chat client."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter
import requests
import configparser
import time

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
			else:
				BUFFER += client_socket.recv(MAXSIZE)
		except OSError:  # Possibly client has left the chat.
			break
	msg_list.insert(tkinter.END, 'Disconnected from server...')


def send(event=None):  # event is passed by binders.
	"""Handles sending of messages."""
	msg = my_msg.get()
	my_msg.set("")	# Clears input field.
	if msg == 'EXIT':
		client_socket.sendall(make_message('EXIT'))
		client_socket.close()
		top.quit()
	elif msg == 'UPDATE':
		client_socket.sendall(make_message('UPDATE'))
	elif len(msg) > 3 and msg[0] == '/' and msg[1] == '/':
		client_socket.sendall(make_message('FAMILY', msg.lstrip('/')))
	elif len(msg) > 2 and msg[0] == '/':
		target, message = msg[1:].split(' ', maxsplit = 1)
		client_socket.sendall(make_message('PRIVATE', f'{target}:{message}'))
	elif msg != '':
		client_socket.sendall(make_message('PUBLIC', msg))


def on_closing(event=None):
	"""This function is to be called when the window is closed."""
	my_msg.set("EXIT")
	send()

top = tkinter.Tk()
top.title("Chatter")

messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()  # For the messages to be sent.
my_msg.set('')
scrollbar = tkinter.Scrollbar(messages_frame)  # To navigate through past messages.
# Following will contain the messages.
msg_list = tkinter.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()

entry_field = tkinter.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tkinter.Button(top, text="Send", command=send)
send_button.pack()

top.protocol("WM_DELETE_WINDOW", on_closing)

while True:
	try:
		r = requests.get('http://localhost:8000/get_world_map').json()
		break
	except requests.exceptions.ConnectionError:
		print('Could not find configuration server, retrying in 5 seconds...')
		time.sleep(5)

#----Now comes the sockets part----
world = input('world: ')
HOST = r[world]['chatserver']['ip']
PORT = r[world]['chatserver']['port']

ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

name = input('name: ')
top.title(name)

client_socket.send(make_message('REGISTER', name))


receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()	# Starts GUI execution.
