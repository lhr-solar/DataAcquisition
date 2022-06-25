from influxdb_client import Point
from influxdb_client.client.write_api import SYNCHRONOUS
import os
import math
import pandas
import time
import logging

output_path = 'IMU.csv'

def IMUparse(input, LOGGING):

    data = ["Accelerometer", "Magnetometer", "Gyroscope"]
    data_field = ['x', 'y', 'z']

    parsed = {
        'Time': time.time(),
        'Accelerometer': {'x': input[0:2], 'y': input[2:4], 'z': input[4:6]},
        'Magnetometer': {'x': input[6:8], 'y': input[8:10], 'z': input[10:12]},
        'Gyroscope': {'x': input[12:14], 'y': input[14:16], 'z': input[16:18]}
    }

    if (LOGGING):
        pandas.DataFrame([parsed])
        pandas.DataFrame.to_csv(output_path, mode='a', header=not os.path.exists(output_path))

    """
    TODO: IMU parsing is broken - 'parsed[i]' in the list comprehension tries to index an int 
        as the key to a dict 'parsed'. :^(
    """


    #return [Point(parsed.keys()[i]).field(parsed[i].keys()[j], parsed[i][j]) for i in parsed for j in ]
    return [Point(data[math.floor(i/3)]).field(data_field[i%3], parsed[i]) for i in range(0,9)]
