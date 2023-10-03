from influxdb_client import Point
from influxdb_client.client.write_api import SYNCHRONOUS
import logging
import math


def IMUparse(input):
    print("Input for IMUparse: ", input) # ^ I added for test
    # logging.basicConfig(filename="log.txt")

    data = ["Accelerometer", "Magnetometer", "Gyroscope"]
    data_field = ["x", "y", "z"]
    # for i in range(0, 9):
    #     # logging.debug

    #     logging.debug(
    #         data[i//3] 
    #         + " "
    #         + data_field[i % 3]
    #         + ": "
    #         + str(int.from_bytes(input[(i * 2) : ((i * 2) + 2)], "little", signed="True"))
    #     )
    # logging.debug("\n")

    # return one point for each
    accel = []
    magnet = []
    gyro = []
   
    returnPoints = [Point(data[i//3]).field(
            data_field[i % 3],
            int.from_bytes(input[(i * 2) : ((i * 2) + 2)], "little", signed="True"),
        )
        for i in range(0, 9)]
    
    for i in range (0, 9):
        if (i % 3 == 0):
            accel.append( int.from_bytes(input[(i * 2) : ((i * 2) + 2)] ))

        elif (i % 3 == 1):
            magnet.append( int.from_bytes(input[(i * 2) : ((i * 2) + 2)] ) )

        elif (i % 3 == 2):
            gyro.append( int.from_bytes(input[(i * 2) : ((i * 2) + 2)] ) )

    # range 0-9
        # process data
        # once we have processed all 

    return returnPoints
