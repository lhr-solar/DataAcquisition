import socket
import logging

HOST = '10.5.0.5'
PORT = 65432

def sender():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    logging.debug("Client starting...")
    s.setblocking(True)
    
    while True:
        data = "test"
        s.sendall(data.encode())
        logging.debug("Data sent.")
        
if __name__ == "__main__":
    sender()
