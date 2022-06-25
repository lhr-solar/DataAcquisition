#!/usr/bin/env python3

from distutils.log import debug
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import socket
import os
import logging
import csv

import can
import gps
import imu
import test

HOST = '' #This listens to every interface
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)
IMU_ID = 1
GPS_ID = 2
CAN_ID = 3
LOGGING = 0

s = socket.create_server(address=(HOST, PORT), family=socket.AF_INET)

def connect_socket():

    logging.debug(f"Server listening on {HOST}")
    s.listen(1)
    (conn, addr) = s.accept()
    logging.debug(f"Server accepted {addr}")
    return conn

def receiver():

    logging.debug("Server starting...")
    s.setblocking(True)
    conn = connect_socket()

    client = InfluxDBClient(url="http://influxdb:8086", token=os.environ.get("DOCKER_INFLUXDB_INIT_ADMIN_TOKEN").strip(), org=os.environ.get("DOCKER_INFLUXDB_INIT_ORG").strip())
    logging.debug("created client")
    write_api = client.write_api(write_options=SYNCHRONOUS)    

    buf = bytearray(2)

    parser = {IMU_ID: imu.IMUparse, GPS_ID: gps.GPSparse, CAN_ID: can.CANparse}
    while(1):
        if (conn.recv_into(buf, 2) == 0):
            logging.warning("Server Disconnected")
            conn = connect_socket(s)
        ethId = int.from_bytes([buf[0]], "little")
        length = int.from_bytes([buf[1]], "little")
        #put CAN/IMU/GPS message into bytearray
        #necessary as recv might not always return the given bytes
        r = bytearray()  
        i = length
        while(i > 0):
            r += bytearray(conn.recv(i))
            i -= len(r)
        write_api.write(bucket="LHR", record=parser[ethId](r)(LOGGING))
        
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    receiver()
    #test.main_test()
