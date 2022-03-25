#!/usr/bin/env python3
#works with echo-server4
import socket

#HOST = socket.gethostbyname(socket.gethostname())
HOST = "169.254.147.123"
PORT = 65432
LENGTH = 64
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "DISCONNECT"

def send(msg):
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.connect((HOST, PORT))
		message = msg.encode(FORMAT)
		msg_length = len(message)
		send_length = str(msg_length).encode(FORMAT)
		send_length += b' ' * (LENGTH - len(send_length))
		s.send(send_length)
		s.send(message)
		print(s.recv(1024).decode(FORMAT))  
		#encoding in a way that can be transmitted over ethernet

binary = input('enter a number: ')
#for digit in binary:
		#decimal = decimal*2 + int(digit)
#number = int(binary, 2)
send(binary)
input()
#send("DISCONNECT")
#print(f"Received {data!r}")
#111100000001000000100000001000000001
#=64441418241 is test number to send for bps trip
#put 4 ones in front just to avoid the leading zeros issue
