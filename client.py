#!/usr/bin/env python3

import socket
import time

#HOST = socket.gethostbyname(socket.gethostname())
HOST = "192.168.137.190"
PORT = 65432
LENGTH = 64
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "DISCONNECT"


def send(msg):
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.connect((HOST, PORT))
		s.send(msg)
		print(s.recv(1024).decode(FORMAT))

#send(bytes([0x3, 0x7, 0x1, 0x5, 0x4, 0x0, 0x0, 0x0, 0x1C, 0x1, 0x12, 0x0, 0x5, 0x0, 0x2, 0x0, 0xD, 0x1, 0x3, 0x0, 0x3, 0x4, 0x4, 0x1, 0x5, 0x9, 0x9, 0x4, 0x0]))		#CAN test

'''
time.sleep(10)
send(bytes([0x1, 0x12, 0x0, 0x5, 0x0, 0x2, 0x0, 0xD, 0x1, 0x3, 0x0, 0x3, 0x4, 0x4, 0x1, 0x5, 0x9, 0x9, 0x4, 0x0]))		#IMU test
#0x31 to 0x39
'''
send(bytes([0x2, 0x2D, 0x42, 0x5A, 0x39, 0x38, 0x37, 0x33, 0x35, 0x31, 0x34, 0x32, 0x31, 0x33, 0x34, 0x35, 0x31, 0x34, 0x32, 0x31, 0x33, 0x34, 0x35, 0x31, 0x34, 0x32, 0x31, 0x33, 0x43, 0x35,
0x31, 0x34, 0x32, 0x31, 0x33, 0x34, 0x35, 0x31, 0x34, 0x32, 0x31, 0x33, 0x34, 0x35, 0x31, 0x34, 0x32]))		#GPS test



