#!/usr/bin/env python3
#run in putty
import socket

#HOST = socket.gethostbyname(socket.gethostname())
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
print(s.getsockname()[0])
HOST = s.getsockname()[0]
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)
LENGTH = 64
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "DISCONNECT"
#multiplies to isolate byte identities
xidentifier = str(111111111111000000000000000000000000) # item to mask for identifier, needs to be string for decima>
xdatalength = str(111100000000111111110000000000000000) # data length multiplier to signify data to read
xfirstdatabyte = str(111100000000000000001111111100000000)
xseconddatabyte = str(111100000000000000000000000011111111)
#data lengths
datalengthis2 = str(111100000000000000100000000000000000)
#all the CAN masks
CANidentity = str(111100000001000000000000000000000000) #result if identity is CAN
BPStripidentity = str(111100000000000000000000001000000000)
BPStrip = str(111100000000000000000000000000000001)
def handle_client(conn, addr):
    print(f"Connected by {addr}")
    connected = True
    while connected:
        msg_length = conn.recv(LENGTH).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            ryan = int(msg)
            ryan1 = ryan & int(xidentifier, 2) #this is where mask occurs, need to convert binary to decimal for com>
            if ryan1 ==  int(CANidentity, 2):
                print(f"{addr} CAN.")
                ryan2 = ryan & int(xdatalength, 2)
                if ryan2 == int(datalengthis2, 2):
                    print(f"{addr} Reading 2 bytes of data...")
                    ryan3 = ryan & int(xfirstdatabyte, 2)
                    if ryan3 == int(BPStripidentity,2):
                        print(f"{addr} BPS trip")
                        ryan4 = ryan & int(xseconddatabyte)
                        if ryan4 == int(BPStrip, 2):
                            print(f"{addr} BPS has tripped!")
            if msg == DISCONNECT_MESSAGE:
                print(f"{addr} disconnected.")
                connected = False

            print(f"{addr}: {ryan1}") #just to check what the outcome is
            conn.send("Msg received". encode(FORMAT))

def start():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Server listening on {HOST}")
        conn, addr = s.accept()

print("Server starting...")
start()