#!/usr/bin/env python3

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

import time
import random
import socket
import os
import logging

import can
import gps
import imu

HOST = '' #This listens to every interface
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)
BYTE = 1
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "DISCONNECT"

async def tester():
    bucket = "LHR"

    client = InfluxDBClient(url="http://influxdb:8086", token=os.environ.get("DOCKER_INFLUXDB_INIT_ADMIN_TOKEN").strip(), org=os.environ.get("DOCKER_INFLUXDB_INIT_ORG").strip())
    write_api = client.write_api(write_options=SYNCHRONOUS)

    while True:
        try:
            r = []

            t1 = Point("Temperature").field("Object 1", (random.randrange(0, 100) / 100) * 30 + 30)
            t2 = Point("Temperature").field("Object 2", (random.randrange(0, 100) / 100) * 30 + 30)
            r += [t1, t2]

            sv = Point("Voltage").field("Supplemental", (random.randrange(0, 100) / 100) * 9 + 6)
            v1 =  Point("Voltage").field("Object 1", (random.randrange(0, 100) / 100) * 9 + 6)
            v2 =  Point("Voltage").field("Object 2", (random.randrange(0, 100) / 100) * 9 + 6)
            r += [sv, v1, v2]

            b = Point("State of Charge").field("Battery", random.randrange(0, 100) / 100 * 100)
            r += [b]

            c = Point("Current").field("Car", random.randrange(-20000, 55000))
            r += [c]

            write_api.write(bucket=bucket, record=r)
        except Exception:
            pass
        time.sleep(.2)
        
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
        array = []
        i = length
        while(i > 0):
            received = bytearray(conn.recv(i))
            array += received
            i -= len(received)
        
        if ethId == 1:
            r = imu.IMUparse(array)
        elif ethId == 2:
            r = gps.GPSparse(array)
        if ethId == 3:
            r = can.CANparse(array)
        
        write_api.write(bucket="LHR", record=r)

if __name__ == "__main__":
    main()
