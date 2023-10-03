
# TODO: Figure out how to test the CAN.Parse function
# TODO:     see what you need to do for CAN.Parse to allow CAN_Test_Data as input


from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS


import socket
import os
import logging

import can
import gps
import imu
import cProfile


def testCAN():
    CAN_Test_Data = bytearray(b'\x16\x06\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00')

    x = 1000000

    for i in range (x):
        if i % 2 == 0:
            can.CANparse(CAN_Test_Data)

        else:
            can.CANparse(CAN_Test_Data)
    
    return

def testIMU():

    IMU_Test_Data = bytearray(b'A\x03\x88\xff\xa8\x02\xa9\xff\xe7\x03\xd4\x01\x8a\xfe\xbd\xfe4\x02')
    x = 1000000

    for i in range (x):
        if i % 2 == 0:
            imu.IMUparse(IMU_Test_Data)
        else:
            imu.IMUparse(IMU_Test_Data)
    
    return


def testGPS():
    x = 1000000

    GPS_Test_Data1 = bytearray(b'064951000A3855.684N09540.619W0.00034.760000000000000')

    for i in range (x):
        if i % 2 == 0:
            gps.GPSparse(GPS_Test_Data1)
        else:
            gps.GPSparse(GPS_Test_Data1)

    return

# cProfile.run("testCAN()")
cProfile.run("testIMU()")
# cProfile.run("testGPS()")




