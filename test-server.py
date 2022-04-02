#!/usr/bin/env python3
import socket
#HOST = socket.gethostbyname(socket.gethostname())
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
print(s.getsockname()[0])
HOST = s.getsockname()[0]
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)
BYTE = 1
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "DISCONNECT"
f = open("message.txt", "w")
def IMUparse(data):
    pass
def GPSparse(data):
    pass
def RTCparse(data):
    pass
def CANparse(data):
    pass
def handle_client(conn, addr):
    print(f"Connected by {addr}")
    for i in range(0, 5):
        f.write(str(conn.recv(BYTE)))
    f.close()
        #if id is None:
        #    continue
'''
length = conn.recv(BYTE)
length = int.from_bytes(length, "big")
id = int.from_bytes(id, "big")
data = conn.recv(length)
if id == 1:
    print(f"ID: IMU")
    IMUparse(data)
elif id == 2:
    print(f"ID: GPS")
    GPSparse(data)
elif id == 3:
    print(f"ID: RTC")
    RTCparse(data)
elif id == 4:
    print(f"ID: CAN")
    CANparse(data)
else:
    continue
print(f"Length: {length}")
print(f"Data: {data}")
f.write("ID: " + str(id))
f.write("\n")
f.write("Length: " + str(length))
f.write("\n")
f.write("Data: " + str(data))
'''
def start():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Server listening on {HOST}")
        conn, addr = s.accept()
        with conn:
            handle_client(conn, addr)
print("Server starting...")
start()