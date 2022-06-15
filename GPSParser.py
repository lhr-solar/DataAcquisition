from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import os
import asyncio

async def GPSparse(array):
    hr = int.from_bytes(array[0:2], "little")
    min = int.from_bytes(array[2:4], "little")
    ms = int.from_bytes(array[4:7], "little")
    latitude_Deg = int.from_bytes(array[7:9], "little")
    latitude_Min = int.from_bytes(array[9:15], "little")
    NorthSouth = int.from_bytes(array[15:16], "little")
    longitude_Deg = int.from_bytes(array[16:19], "little")
    longitude_Min = int.from_bytes(array[19:25], "little")
    EastWest = int.from_bytes(array[25:26], "little")
    speedInKnots = int.from_bytes(array[26:30], "little")
    day = int.from_bytes(array[30:32], "little")
    month = int.from_bytes(array[32:34], "little")
    year = int.from_bytes(array[34:38], "little")
    magneticVariation_Deg = int.from_bytes(array[38:42], "little")
    magneticVariation_EastWest = int.from_bytes(array[42:43], "little")
    print(f"hr: {hr}")
    print(f"min: {min}")
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

    bucket = "LHR"
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
