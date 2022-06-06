#comment out to write to the dashboard
'''
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import asyncio
import os
'''

# typedef struct{
#     char hr[2]; // Will not use these parameters unless we have to
#     char min[2]; // ^^
#     char sec[2]; // ^^
#     char ms[3]; // ^^
#     char latitude_Deg[2];
#     char latitude_Min[6];
#     char NorthSouth;
#     char longitude_Deg[3];
#     char longitude_Min[6];
#     char EastWest;
#     char speedInKnots[4];
#     char day[2]; // Will not use these parameters unless we have to
#     char month[2]; // ^^
#     char year[4]; // ^^
#     char magneticVariation_Deg[4];
#     char magneticVariation_EastWest;
# } GPSData_t;

import secrets

def GPSparse(data):
    bucket = "LHR"

    hr = chr(data[0]) + chr(data[1])
    min = chr(data[2]) + chr(data[3])
    sec = chr(data[4]) + chr(data[5])
    ms = chr(data[6]) + chr(data[7]) + chr(data[8]) 
    latitude_Deg = chr(data[9]) + chr(data[10]) 
    latitude_Min = chr(data[11]) + chr(data[12]) + chr(data[13]) + chr(data[14]) + chr(data[15]) + chr(data[16])  
    NorthSouth = chr(data[17])
    longitude_Deg = chr(data[18]) + chr(data[19]) + chr(data[20])  
    longitude_Min = chr(data[21]) + chr(data[22]) + chr(data[23]) + chr(data[24]) + chr(data[25]) + chr(data[26])   
    EastWest = chr(data[27]) 
    speedInKnots = chr(data[28]) + chr(data[29]) + chr(data[30]) + chr(data[31])   
    day = chr(data[32]) + chr(data[33])  
    month = chr(data[34]) + chr(data[35])  
    year = chr(data[36]) + chr(data[37]) + chr(data[38]) + chr(data[39])  
    magneticVariation_Deg = chr(data[40]) + chr(data[41]) + chr(data[42]) + chr(data[43]) 
    magneticVariation_EastWest = chr(data[44])

    #comment out if testing on local computer
    print("Payload: " + data + "\n")
    print(f"hr: {hr}")
    print(f"min: {min}")
    print(f"sec: {sec}")
    print(f"ms: {ms}")
    print(f"latitude_Deg: {latitude_Deg}")
    print(f"latitude_Min: {latitude_Min}")
    print(f"NorthSouth: {NorthSouth}")
    print(f"longitude_Deg: {longitude_Deg}")
    print(f"longitude_Min: {longitude_Min}")
    print(f"EastWest: {EastWest}")
    print(f"speedInKnots: {speedInKnots}")
    print(f"day: {day}")
    print(f"month: {month}")
    print(f"year: {year}")
    print(f"magneticVariation_Deg: {magneticVariation_Deg}")
    print(f"magneticVariation_EastWest: {magneticVariation_EastWest}")

    #comment out to write to the dashboard
    '''
    while True:
        try:
            r = []
            client = InfluxDBClient(url="http://influxdb:8086", token=os.environ.get("DOCKER_INFLUXDB_INIT_ADMIN_TOKEN").strip(), org=os.environ.get("DOCKER_INFLUXDB_INIT_ORG").strip())
            write_api = client.write_api(write_options=SYNCHRONOUS)
            query_api = client.query_api()

            g1 = Point("hr").field(hr)
            g2 = Point("min").field(min)
            g3 = Point("ms").field(ms)
            g4 = Point("latitute_Deg").field(latitude_Deg)
            g5 = Point("latitude_Min").field(latitude_Min)
            g6 = Point("NorthSouth").field(NorthSouth)
            g7 = Point("longitude_Deg").field(longitude_Deg)
            g8 = Point("longitude_Min").field(longitude_Min)
            g9 = Point("EastWest").field(EastWest)
            g10 = Point("speedInKnots").field(speedInKnots)
            g11 = Point("day").field(day)
            g12 = Point("year").field(year)
            g13 = Point("month").field(month)
            g14 = Point("magneticVariation_Deg").field(magneticVariation_Deg)
            g15 = Point("magneticVariation_EastWest").field(magneticVariation_EastWest)

            r += [g1, g2, g3, g4, g5, g6, g7, g8, g9, g10, g11, g12, g13, g14, g15]


            write_api.write(bucket=bucket, record=r)

        except Exception:
            pass
        await asyncio.sleep(.2)
    '''
