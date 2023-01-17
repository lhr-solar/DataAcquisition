#!/usr/bin/env python3

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import socket
import os
import logging

import can
import gps
import imu

HOST = ""  # This listens to every interface
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)
IMU_ID = 1
GPS_ID = 2
CAN_ID = 3


def connect_socket(s: socket) -> socket:

    logging.warning(f"Server listening on {HOST}")
    s.listen(1)
    (conn, addr) = s.accept()
    logging.warning(f"Server accepted {addr}")
    return conn


def reconnect_socket(server: socket, conn: socket) -> socket:

    logging.warning("Server Disconnected")
    conn.close()
    return connect_socket(server)


class ServerDisconnectError(Exception):
    pass


def receiver():

    s = socket.create_server(address=(HOST, PORT), family=socket.AF_INET)
    logging.warning("Server starting...")
    s.setblocking(True)
    conn = connect_socket(s)

    client = InfluxDBClient(
        url="http://influxdb:8086",
        token=os.environ.get("DOCKER_INFLUXDB_INIT_ADMIN_TOKEN").strip(),
        org=os.environ.get("DOCKER_INFLUXDB_INIT_ORG").strip(),
    )
    logging.warning("Influx client created.")
    write_api = client.write_api(write_options=SYNCHRONOUS)

    buf = bytearray(4096)

    parser = {IMU_ID: imu.IMUparse, GPS_ID: gps.GPSparse, CAN_ID: can.CANparse}
    while True:
        try:
            if conn.recv_into(buf, 2) == 0:
                logging.warning("Empty")
                raise ServerDisconnectError

            ethID = int.from_bytes([buf[0]], "little")
            length = int.from_bytes([buf[1]], "little")
            if ethID not in parser:
                logging.warning("Wrong ID")
                raise ServerDisconnectError

            # put CAN/IMU/GPS message into bytearray
            # necessary as recv might not always return the given bytes
            r = bytearray(length)
            i = 0
            while i < length:
                recv_len = conn.recv_into(buf, length - i)
                if recv_len == 0:
                    logging.warning("Empty Packet")
                    raise ServerDisconnectError
                r[i : recv_len + i] = buf[:recv_len]
                i += recv_len

            write_api.write(bucket="LHR", record=parser[ethID](r))
        except ServerDisconnectError:
            conn = reconnect_socket(s, conn)


if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING)
    receiver()
