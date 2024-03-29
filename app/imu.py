from influxdb_client import Point
from influxdb_client.client.write_api import SYNCHRONOUS
import logging
import math


def IMUparse(input):
    data = ["Accelerometer", "Magnetometer", "Gyroscope"]
    data_field = ["x", "y", "z"]
    for i in range(0, 9):
        logging.debug(
            data[math.floor(i / 3)]
            + " "
            + data_field[i % 3]
            + ": "
            + str(int.from_bytes(input[(i * 2) : ((i * 2) + 2)], "little", signed="True"))
        )
    logging.debug("\n")

    return [
        Point(data[math.floor(i / 3)]).field(
            data_field[i % 3],
            int.from_bytes(input[(i * 2) : ((i * 2) + 2)], "little", signed="True"),
        )
        for i in range(0, 9)
    ]
