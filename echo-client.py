import socket

#HOST = socket.gethostbyname(socket.gethostname())
HOST = "169.254.48.219"
PORT = 65432
LENGTH = 64
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "DISCONNECT"
BYTE = 1

def send(msg):
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.connect((HOST, PORT))
		s.send(msg)
		print(s.recv(1024).decode(FORMAT))

send(bytes([0x3, 0x9, 0x4, 0x1, 0x5, 0x1, 0x2, 0x3, 0x4, 0x0, 0x0]))

#send(DISCONNECT_MESSAGE)
#print(f"Received {data!r}")
