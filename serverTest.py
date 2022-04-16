import socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
print(s.getsockname()[0])
HOST = s.getsockname()[0]
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)
BYTE = 1
FORMAT = 'utf-8'

def handle_client(conn, addr):
    print(f"Connected by {addr}")
    conn.send([0x1, 0x2, 0x3, 0x4]) #send data to client

def start():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Server listening on {HOST}")
        conn, addr = s.accept()
        with conn:
            handle_client(conn, addr)


print("Server starting...")
print("HOST:" + HOST)
start()