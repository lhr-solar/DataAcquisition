from influxdb_client import Point
from influxdb_client.client.write_api import SYNCHRONOUS
import os
import time
import logging
import sys
import csv

def IMUparse(input: bytearray):

    points = [(i, j) for i in ('Accelerometer', 'Magnetometer', 'Gyroscope') for j in 'xyz']
    parsed = [int.from_bytes(input[2*i:2*i+2], 'little') for i in range(9)]
    parsed += time.time()

    return [Point(points[i][0]).field(points[i][1], parsed[i]) for i in range(len(parsed)-1)]
