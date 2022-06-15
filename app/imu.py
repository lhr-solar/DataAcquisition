from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import asyncio
import os

async def IMUparse(array):
    accelx = array[0:2]
    accelx = int.from_bytes(accelx, "little")
    #print(f"Accelx: {accelx}")  #printing just for testing purposes

    accely = array[2:4]
    accely = int.from_bytes(accely, "little")
    #print(f"Accely: {accely}")

    accelz = array[4:6]
    accelz = int.from_bytes(accelz, "little")
    #print(f"Accelz: {accelz}")

    magx = array[6:8]
    magx = int.from_bytes(magx, "little")
    #print(f"Magx: {magx}")

    magy = array[8:10]
    magy = int.from_bytes(magy, "little")
    #print(f"Magy: {magy}")

    magz = array[10:12]
    magz = int.from_bytes(magz, "little")
    #print(f"Magz: {magz}")

    gyrx = array[12:14]
    gyrx = int.from_bytes(gyrx, "little")
    #print(f"Gyrx: {gyrx}")

    gyry = array[14:16]
    gyry = int.from_bytes(gyry, "little")
    #print(f"Gyry: {gyry}")

    gyrz = array[16:18]
    gyrz = int.from_bytes(gyrz, "little")
    #print(f"Gyrz: {gyrz}")

    bucket = "LHR"
    try:
        r = []

        a1 = Point("Accelerometer").field("x", accelx)
        a2 = Point("Accelerometer").field("y", accely)
        a3 = Point("Accelerometer").field("z", accelz)
        r += [a1, a2, a3]

        m1 = Point("Magnetometer").field("x", magx)
        m2 = Point("Magnetometer").field("y", magy)
        m3 = Point("Magnetometer").field("z", magz)
        r += [m1, m2, m3]

        g1 = Point("Gyroscope").field("x", gyrx)
        g2 = Point("Gyroscope").field("y", gyry)
        g3 = Point("Gyroscope").field("z", gyrz)
        r += [g1, g2, g3]

        return r