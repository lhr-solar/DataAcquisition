#comment out to write to the dashboard

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import asyncio
import os

from locale import locale_encoding_alias
import secrets

#comment out if you want to test -need to fix test
#data = [0x2, 0x2D, 0x31, 0x34, 0x2, 0x1, 0x3, 0x4, 0x5, 0x31, 0x34, 0x2, 0x1, 0x3, 0x4, 0x5, 0x31, 0x34, 0x2, 0x1, 0x3, 0x4, 0x5, 0x31, 0x34, 0x2, 0x1, 0x3, 0x4, 0x5,
#0x31, 0x34, 0x2, 0x1, 0x3, 0x4, 0x5, 0x31, 0x34, 0x2, 0x1, 0x3, 0x4, 0x5, 0x31, 0x34, 0x2, 0x4, 0x5, 0x31, 0x34, 0x2, 0x34, 0x2, 0x4, 0x5, 0x31, 0x34, 0x2]

def GPSparse(data):
    bucket = "LHR"
    
    time = chr(data[1]) + chr(data[2]) + chr(data[3])+ chr(data[4])+ chr(data[5])+ chr(data[6])+ chr(data[7])+ chr(data[8])+ chr(data[9])
    status = chr(data[10])
    latitude = chr(data[11]) + chr(data[12])+ chr(data[13])+ chr(data[14])+ chr(data[15])+ chr(data[16])+ chr(data[17])+ chr(data[18])
    NorthSouth = chr(data[19])
    longitude = chr(data[20]) + chr(data[21]) + chr(data[22])+ chr(data[23])+ chr(data[24])+ chr(data[25])+ chr(data[26])+ chr(data[27])+ chr(data[28]) 
    EastWest = chr(data[29]) 
    speedInKnots = chr(data[30]) + chr(data[31]) + chr(data[32]) + chr(data[33])
    courseInDegrees = chr(data[34]) + chr(data[35]) + chr(data[36])+ chr(data[37]) + chr(data[38]) + chr(data[39])
    date = chr(data[40]) + chr(data[41]) + chr(data[42]) + chr(data[43]) + chr(data[44]) + chr(data[45])   
    magneticVariation = chr(data[46]) + chr(data[47]) + chr(data[48]) + chr(data[49]) + chr(data[50]) + chr(data[51]) + chr(data[52])

    #comment out if testing on local computer
    print("Payload: " + data + "\n")
    print(f"time: {time}")
    print(f"status: {status}")
    print(f"latitude: {latitude}")
    print(f"NorthSouth: {NorthSouth}")
    print(f"longitude: {longitude}")
    print(f"EastWest: {EastWest}")
    print(f"speedInKnots: {speedInKnots}")
    print(f"courseInDegrees: {courseInDegrees}")
    print(f"date: {date}")
    print(f"magneticVariation: {magneticVariation}")
    print(f"speedInKnots: {speedInKnots}")

#if testing
#GPSparse(data)

    #comment out to write to the dashboard
    while True:
        try:
            r = []
            client = InfluxDBClient(url="http://influxdb:8086", token=os.environ.get("DOCKER_INFLUXDB_INIT_ADMIN_TOKEN").strip(), org=os.environ.get("DOCKER_INFLUXDB_INIT_ORG").strip())
            write_api = client.write_api(write_options=SYNCHRONOUS)
            query_api = client.query_api()
            g1 = Point("time").field(time)
            g2 = Point("status").field(status)
            g3 = Point("latitude").field(latitude)
            g4 = Point("NorthSouth").field(NorthSouth)
            g5 = Point("longitude").field(longitude)
            g6 = Point("EastWest").field(EastWest)
            g7 = Point("speedInKnots").field(speedInKnots)
            g8 = Point("courseInDegrees").field(courseInDegrees)
            g9 = Point("date").field(date)
            g10 = Point("magneticVariation").field(magneticVariation)
            r += [g1, g2, g3, g4, g5, g6, g7, g8, g9, g10]
            write_api.write(bucket=bucket, record=r)
        except Exception:
            pass
        await asyncio.sleep(.2)