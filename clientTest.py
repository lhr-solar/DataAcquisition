import socket

#HOST = socket.gethostbyname(socket.gethostname())
HOST = "169.254.48.219"
PORT = 9873
LENGTH = 64
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "DISCONNECT"
BYTE = 1
f = open("message.txt", "w")

def interpretData():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        id = s.recv(BYTE)
        length = s.recv(BYTE)
        length = int.from_bytes(length, "big")
        id = int.from_bytes(id, "big")
        data = s.recv(length) 
        f.write("ID: " + str(id))
        f.write("Length: " + str(length))
        f.write("Data: " + str(data))
        f.close()

while(True):
    try:
        interpretData()
    except:
        continue
