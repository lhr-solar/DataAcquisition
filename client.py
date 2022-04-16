#!/usr/bin/env python3

import socket

#HOST = socket.gethostbyname(socket.gethostname())
HOST = "169.254.95.217"
PORT = 65432
LENGTH = 64
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "DISCONNECT"

def send(msg):
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.connect((HOST, PORT))
		s.send(msg)
		print(s.recv(1024).decode(FORMAT))

send(bytes([0x3, 0x7, 0x1, 0x2, 0x4, 0x1, 0x2, 0x3, 0x4]))		# b'\0x1\0x2'
