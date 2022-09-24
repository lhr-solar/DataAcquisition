import logging
import socket


HOST = 'localhost' #runs local host
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)
IMU_ID = 1
GPS_ID = 2
CAN_ID = 3

def connect_socket(s: socket) -> socket:

    logging.debug(f"Server listening on {HOST}")
    s.listen(1)
    (conn, addr) = s.accept()
    logging.debug(f"Server accepted {addr}")
    return conn

def reconnect_socket(server: socket, conn: socket) -> socket:
    
    logging.warning("Server Disconnected")
    conn.close()
    return connect_socket(server)

class ServerDisconnectError(Exception): pass

def receiver():

    s = socket.create_server(address=(HOST, PORT), family=socket.AF_INET)
    logging.debug("Server starting...")
    s.setblocking(True)
    conn = connect_socket(s)
    buf = bytearray(4096)

    #parser = {IMU_ID: imu.IMUparse, GPS_ID: gps.GPSparse, CAN_ID: can.CANparse}
    while True:
        try:
            if conn.recv_into(buf, 2) == 0:
                raise ServerDisconnectError
            
            ethID = int.from_bytes([buf[0]], "little")
            length = int.from_bytes([buf[1]], "little")
            #if ethID not in parser:
                #raise ServerDisconnectError

            # put CAN/IMU/GPS message into bytearray
            # necessary as recv might not always return the given bytes
            r = bytearray(length)  
            i = 0
            while i < length:
                recv_len = conn.recv_into(buf, length-i)
                if recv_len == 0:
                    raise ServerDisconnectError
                r[i:recv_len+i] = buf[:recv_len]
                i += recv_len
            logging.debug(r)
        except ServerDisconnectError:
            conn = reconnect_socket(s, conn)

        
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    receiver()