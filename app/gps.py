from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import asyncio
import os

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

async def GPSparse(data):
    bucket = "LHR"
    hr = ord(int.from_bytes(data[0], "little")) + ord(int.from_bytes(data[1], "little"))
    min = ord(int.from_bytes(data[2], "little")) + ord(int.from_bytes(data[3], "little"))
    sec = ord(int.from_bytes(data[4], "little")) + ord(int.from_bytes(data[5], "little"))
    ms = int.from_bytes(data[6:9], "little")
    latitude_Deg = int.from_bytes(data[9:11], "little")
    latitude_Min = int.from_bytes(data[11:17], "little")
    NorthSouth = int.from_bytes(data[17], "little")
    longitude_Deg = int.from_bytes(data[18:21], "little")
    longitude_Min = int.from_bytes(data[21:27], "little")
    EastWest = int.from_bytes(data[27], "little")
    speedInKnots = int.from_bytes(data[28:32], "little")
    day = int.from_bytes(data[32:34], "little")
    month = data[34:36]
    year = data[36:40]
    magneticVariation_Deg = data[40:44]
    magneticVariation_EastWest = data[44]

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
    print(f"year: {year}")
    print(f"month: {month}")
    print(f"magneticVariation_Deg: {magneticVariation_Deg}")
    print(f"magneticVariation_EastWest: {magneticVariation_EastWest}")

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