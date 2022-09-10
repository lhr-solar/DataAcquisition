from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import os

import can
import gps
import imu
import logging

#All Data is little endian (smallest index of each field has LSB)
CAN_Test_Data = [
#   |         CAN ID       |          IDX          |                     DATA                      |
    [0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01], #Dash Kill Switch On
    [0x00, 0x00, 0x00, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01], #BPS Trip On
    [0x00, 0x00, 0x00, 0x03, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01], #Any System Failure On
    [0x00, 0x00, 0x00, 0x04, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01], #Ignition On
    [0x00, 0x00, 0x00, 0x05, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01], #Any System Shutoff On
    [0x00, 0x00, 0x01, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01], #BPS All Clear Enabled
    [0x00, 0x00, 0x01, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01], #BPS Contactor State On
    [0x00, 0x00, 0x01, 0x03, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x04, 0xFC, 0xF3, 0xFF, 0xFF], #BPS Current
    [0x00, 0x00, 0x01, 0x04, 0x00, 0x00, 0x00, 0x05, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0D, 0x71], #BPS Voltage 3441mV
    [0x00, 0x00, 0x01, 0x05, 0x00, 0x00, 0x00, 0x05, 0x00, 0x00, 0x00, 0x06, 0x00, 0x00, 0x94, 0x32], #BPS Temperature 37000ish
    [0x00, 0x00, 0x01, 0x06, 0x00, 0x00, 0x00, 0x00, 0x04, 0x00, 0x00, 0x00, 0x01, 0x01, 0x01, 0x01], #SOC gibberish
    [0x00, 0x00, 0x01, 0x07, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01], #WDOG Triggered True
    [0x00, 0x00, 0x01, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01], #CAN Error True
    #[0x109] - NOT USED
    [0x00, 0x00, 0x01, 0x0B, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02, 0x0D, 0x31], #Supplemental Voltage 3441mV
    [0x00, 0x00, 0x01, 0x0C, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01], #Charging Enabled

    [0x00, 0x00, 0x05, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01], #Car State On
    [0x00, 0x00, 0x02, 0x42, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0D, 0x71, 0x00, 0x00, 0x0D, 0x71], #Gibberish for these too
    [0x00, 0x00, 0x02, 0x43, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0D, 0x71, 0x00, 0x00, 0x0D, 0x71],
    [0x00, 0x00, 0x02, 0x44, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0D, 0x71, 0x00, 0x00, 0x0D, 0x71],
    [0x00, 0x00, 0x02, 0x45, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0D, 0x71, 0x00, 0x00, 0x0D, 0x71],
    [0x00, 0x00, 0x02, 0x46, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0D, 0x71, 0x00, 0x00, 0x0D, 0x71],
    [0x00, 0x00, 0x02, 0x47, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0D, 0x71, 0x00, 0x00, 0x0D, 0x71],
    [0x00, 0x00, 0x02, 0x4B, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0D, 0x71, 0x00, 0x00, 0x0D, 0x71],
    [0x00, 0x00, 0x02, 0x4E, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0D, 0x71, 0x00, 0x00, 0x0D, 0x71],
    [0x00, 0x00, 0x02, 0x4F, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01], #Array Contactor Enabled

    [0x00, 0x00, 0x06, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0D, 0x71], #More Gibberish
    [0x00, 0x00, 0x06, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0D, 0x71],
    [0x00, 0x00, 0x06, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0D, 0x71],
    [0x00, 0x00, 0x06, 0x03, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0D, 0x71],
    [0x00, 0x00, 0x06, 0x04, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0D, 0x71],
    [0x00, 0x00, 0x06, 0x05, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01], #Sunscatter A override enabled
    [0x00, 0x00, 0x06, 0x06, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01], #Sunscatter A Fault Enabled
    [0x00, 0x00, 0x06, 0x10, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0D, 0x71], #some hoogaboogah
    [0x00, 0x00, 0x06, 0x11, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0D, 0x71],
    [0x00, 0x00, 0x06, 0x12, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0D, 0x71],
    [0x00, 0x00, 0x06, 0x13, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0D, 0x71],
    [0x00, 0x00, 0x06, 0x14, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0D, 0x71],
    [0x00, 0x00, 0x06, 0x15, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01], #Sunscatter B override enabled
    [0x00, 0x00, 0x06, 0x16, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01] #Sunscatter B fault enabled
]

GPS_Test_Data = ["064951000A2307.1256N12016.4438E0.03165.482604063.05W"]

IMU_Test_Data = [
    bytearray(b'\xf8\xfe\x01\x00\xbe\x03\x82\xfc\xaa\xfe\xcc\xfc\x00\x00\xfe\xff\x02\x00'),
    bytearray(b'\xf9\xfe\x00\x00\xbb\x03\x82\xfc\xaa\xfe\xcc\xfc\xfb\xff\xff\xff\x06\x00'),
    bytearray(b'\xfa\xfe\x01\x00\xbe\x03\x82\xfc\xaa\xfe\xcc\xfc\xf3\xff\xfa\xff\x0b\x00')
]

def can_test():
    #This sends everything in little endian
    for i in CAN_Test_Data: return can.CANparse(bytearray(i[3::-1] + i[7:3:-1] + i[16:7:-1]), 1) 

def gps_test():
    gps.GPSparse(GPS_Test_Data)

def imu_test():
    pass

#This is the only function that should be called outside of this file. Other functions will be called within this function
def main_test():
    can_test()

if __name__ == '__main__':
    main_test()