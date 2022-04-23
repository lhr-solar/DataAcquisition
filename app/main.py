#!/usr/bin/env python3

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

import os
import random
import asyncio

import socket
#HOST = socket.gethostbyname(socket.gethostname())
#s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#s.connect(("8.8.8.8", 80))
#print(s.getsockname()[0])
#HOST = s.getsockname()[0]
HOST = "0.0.0.0"
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)
BYTE = 1
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "DISCONNECT"

CANIDs = {
     0x002: "BPS Trip",
     0x101: "BPS All Clear",
     0x102: "BPS Contactor State",
     0x103: "Current Data",
     0x104: "Voltage Data Array",
     0x105: "Temperature Data Array",
     0x106: "State of Charge Data",
     0x107: "WDog Triggered",
     0x108: "CAN Error",
     0x109: "BPS Command msg",
     0x10B: "Supplemental Voltage",
     0x10C: "Charging Enabled",

     0x580: "Car State",
     0x242: "Motor Controller Bus",
     0x243: "Velocity",
     0x244: "Motor Controller Phase Current",
     0x245: "Motor Voltage Vector",
     0x246: "Motor Current Vector",
     0x247: "Motor BackEMF",
     0x24B: "Motor Temperature",
     0x24E: "Odometer & Bus Amp Hours",

     0x600: "Sunscatter A Array Voltage Setpoint",
     0x601: "Sunscatter A Array Voltage Measurement",
     0x602: "Sunscatter A Array Current Measurement",
     0x603: "Sunscatter A Battery Voltage Measurement",
     0x604: "Sunscatter A Battery Current Measurement",
     0x605: "Sunscatter A Override Enabled/Disable command",
     0x606: "Sunscatter A Fault",
     0x610: "Sunscatter B Array Voltage Setpoint",
     0x611: "Sunscatter B Array Voltage Measurement",
     0x612: "Sunscatter B Array Current Measurement",
     0x613: "Sunscatter B Battery Voltage Measurement",
     0x614: "Sunscatter B Battery Current Measurement",
     0x615: "Sunscatter B Override Enabled/Disable command",
     0x616: "Sunscatter B Fault",

     0x620: "Blackbody Measurement",
     0x630: "Blackbody (Irradiance Sensor 1) Measurement",
     0x631: "Blackbody (Irradience Sensor 2) Measurement",
     0x632: "Blackbody (Irradience/RTD) Board Enabled/Disable command",
     0x633: "Blackbody (Irradience/RTD) Board Fault",
     0x640: "PV Curve Tracer Profile",
}

async def tester():
    bucket = "LHR"
    while True:
        try:
            r = []
            client = InfluxDBClient(url="http://influxdb:8086", token=os.environ.get("DOCKER_INFLUXDB_INIT_ADMIN_TOKEN").strip(), org=os.environ.get("DOCKER_INFLUXDB_INIT_ORG").strip())
            write_api = client.write_api(write_options=SYNCHRONOUS)
            query_api = client.query_api()

            t1 = Point("Temperature").field("Object 1", (random.randrange(0, 100) / 100) * 30 + 30)
            t2 = Point("Temperature").field("Object 2", (random.randrange(0, 100) / 100) * 30 + 30)
            r += [t1, t2]

            sv = Point("Voltage").field("Supplemental", (random.randrange(0, 100) / 100) * 9 + 6)
            v1 =  Point("Voltage").field("Object 1", (random.randrange(0, 100) / 100) * 9 + 6)
            v2 =  Point("Voltage").field("Object 2", (random.randrange(0, 100) / 100) * 9 + 6)
            r += [sv, v1, v2]

            b = Point("State of Charge").field("Battery", random.randrange(0, 100) / 100 * 100)
            r += [b]

            c = Point("Current").field("Car", random.randrange(-20000, 55000))
            r += [c]

            write_api.write(bucket=bucket, record=r)
        except Exception:
            pass
        await asyncio.sleep(.2)

def CANparse(canArray):
    canID = int.from_bytes(canArray[0:2], "big")
    index = int.from_bytes(canArray[2:3], "big")
    rawData = int.from_bytes(canArray[3: 7], "big")
    print(CANIDs[canID], str(index), rawData) #will be replaced by writing to database
    bucket = "LHR"
    try:
        r = []
        client = InfluxDBClient(url="http://influxdb:8086", token=os.environ.get("DOCKER_INFLUXDB_INIT_ADMIN_TOKEN").strip(), org=os.environ.get("DOCKER_INFLUXDB_INIT_ORG").strip())
        write_api = client.write_api(write_options=SYNCHRONOUS)
        query_api = client.query_api()
        a1 = Point(CANIDs[canID]).field(index, rawData)
        r += a1    
        write_api.write(bucket=bucket, record=r)
    except Exception:
        pass

def IMUparse(array):
    accelx = array[0:2]
    accelx = int.from_bytes(accelx, "big")
    print(f"Accelx: {accelx}")  #printing just for testing purposes

    accely = array[2:4]
    accely = int.from_bytes(accely, "big")
    print(f"Accely: {accely}")

    accelz = array[4:6]
    accelz = int.from_bytes(accelz, "big")
    print(f"Accelz: {accelz}")

    magx = array[6:8]
    magx = int.from_bytes(magx, "big")
    print(f"Magx: {magx}")

    magy = array[8:10]
    magy = int.from_bytes(magy, "big")
    print(f"Magy: {magy}")

    magz = array[10:12]
    magz = int.from_bytes(magz, "big")
    print(f"Magz: {magz}")

    gyrx = array[12:14]
    gyrx = int.from_bytes(gyrx, "big")
    print(f"Gyrx: {gyrx}")

    gyry = array[14:16]
    gyry = int.from_bytes(gyry, "big")
    print(f"Gyry: {gyry}")

    gyrz = array[16:18]
    gyrz = int.from_bytes(gyrz, "big")
    print(f"Gyrz: {gyrz}")

    bucket = "LHR"
    try:
        r = []
        client = InfluxDBClient(url="http://influxdb:8086", token=os.environ.get("DOCKER_INFLUXDB_INIT_ADMIN_TOKEN").strip(), org=os.environ.get("DOCKER_INFLUXDB_INIT_ORG").strip())
        write_api = client.write_api(write_options=SYNCHRONOUS)
        query_api = client.query_api()

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
    
        write_api.write(bucket=bucket, record=r)
    except Exception:
        pass

def GPSparse(data):
    bucket = "LHR"
    hr = ord(int.from_bytes(data[0], "big")) + ord(int.from_bytes(data[1], "big"))
    min = ord(int.from_bytes(data[2], "big")) + ord(int.from_bytes(data[3], "big"))
    sec = ord(int.from_bytes(data[4], "big")) + ord(int.from_bytes(data[5], "big"))
    ms = int.from_bytes(data[6:9], "big")
    latitude_Deg = int.from_bytes(data[9:11], "big")
    latitude_Min = int.from_bytes(data[11:17], "big")
    NorthSouth = int.from_bytes(data[17], "big")
    longitude_Deg = int.from_bytes(data[18:21], "big")
    longitude_Min = int.from_bytes(data[21:27], "big")
    EastWest = int.from_bytes(data[27], "big")
    speedInKnots = int.from_bytes(data[28:32], "big")
    day = int.from_bytes(data[32:34], "big")
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

def handle_client(conn, addr):

    print(f"Connected by {addr}")
    while(1):
        ethId = int.from_bytes(conn.recv(1), "big")
        length = int.from_bytes(conn.recv(1), "big")

        #put CAN/IMU/GPS message into bytearray
        #necessary as recv might not always return the given bytes
        array = []
        i = length
        while(i > 0):
            received = bytearray(conn.recv(i))
            array += received
            i -= len(received)

        if ethId == 1:
            print(f"ID: IMU")
            IMUparse(array)
        elif ethId == 2:
            print(f"ID: GPS")
            GPSparse(array)
        elif ethId == 3:
            print(f"ID: CAN")
            CANparse(array)


def start():
    print("Server starting...", flush=True)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Server listening on {HOST}")
        conn, addr = s.accept()
        with conn:
            handle_client(conn, addr)
"""
app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

@app.on_event("startup")
async def on_startup():
    #asyncio.create_task(tester()) 
    asyncio.create_task(start())


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    ip = os.environ.get("PI_IP")
    return templates.TemplateResponse("index.html", {"request": request, "ip": ip})
"""

start()