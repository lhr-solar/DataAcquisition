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

def IMUparse(data):
    pass
def GPSparse(data):
    pass
def CANparse(canArray):
    canID = int.from_bytes(canArray[0:2], "big")
    index = int.from_bytes(canArray[2:3], "big")
    rawData = int.from_bytes(canArray[3: 7], "big")
    print(canID, index, rawData)


def handle_client(conn, addr):
    print(f"Connected by {addr}")
    ethId = int.from_bytes(conn.recv(1))
    length = int.from_bytes(conn.recv(1))
    
    #put CAN/IMU/GPS message into bytearray
    #necessary as recv might not always return the given bytes
    array = []
    i = length
    while(i > 0):
        received = bytearray(conn.recv(i))
        array.append(received)
        i - len(received)

    if ethId == 1:
        print(f"ID: IMU")
        IMUparse(array)
    elif ethId == 2:
        print(f"ID: GPS")
        GPSparse(array)
    elif ethId == 3:
        print(f"ID: CAN")
        CANparse(array)

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