#!/usr/bin/env python3

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import socket
import os
import logging

import can
import gps
import imu
import test

HOST = '' #This listens to every interface
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)
        
def connect_socket(s):

    logging.debug(f"Server listening on {HOST}")
    s.listen(1)
    (conn, addr) = s.accept()
    logging.debug(f"Server accepted {addr}")
    return conn

def main():
    logging.basicConfig(level=logging.DEBUG)

    logging.debug("Server starting...")
    s = socket.create_server(address=(HOST, PORT), family=socket.AF_INET)
    s.setblocking(True)
    logging.debug(f"Server listening on {HOST}")
    s.listen(1)
    (conn, addr) = s.accept()
    logging.debug(f"Server accepted {addr}")

    client = InfluxDBClient(url="http://influxdb:8086", token=os.environ.get("DOCKER_INFLUXDB_INIT_ADMIN_TOKEN").strip(), org=os.environ.get("DOCKER_INFLUXDB_INIT_ORG").strip())
    logging.debug("created client")
    write_api = client.write_api(write_options=SYNCHRONOUS)    

    buf = bytearray(2)

    while(1):
        if (conn.recv_into(buf, 2) == 0):
            logging.warning("Server Disconnected")
            conn = connect_socket(s)
        ethId = int.from_bytes([buf[0]], "little")
        length = int.from_bytes([buf[1]], "little")
        #put CAN/IMU/GPS message into bytearray
        #necessary as recv might not always return the given bytes
        received = bytearray()  
        i = length
        while(i > 0):
            received += bytearray(conn.recv(i))
            i -= len(received)

        if ethId == 1:
            r = imu.IMUparse(received)
        elif ethId == 2:
            r = gps.GPSparse(received)
        if ethId == 3:
            r = can.CANparse(received)
        
        write_api.write(bucket="LHR", record=r)

if __name__ == "__main__":
    main()
