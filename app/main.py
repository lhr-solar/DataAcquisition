#!/usr/bin/env python3

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

import os
import random
import threading
import socket

import can
import gps
import imu

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

async def tester():
    bucket = "LHR"

    client = InfluxDBClient(url="http://influxdb:8086", token=os.environ.get("DOCKER_INFLUXDB_INIT_ADMIN_TOKEN").strip(), org=os.environ.get("DOCKER_INFLUXDB_INIT_ORG").strip())
    write_api = client.write_api(write_options=SYNCHRONOUS)
    query_api = client.query_api()
    while True:
        try:
            r = []

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

def handle_client(conn, addr):

    print(f"Connected by {addr}")
    client = InfluxDBClient(url="http://influxdb:8086", token=os.environ.get("DOCKER_INFLUXDB_INIT_ADMIN_TOKEN").strip(), org=os.environ.get("DOCKER_INFLUXDB_INIT_ORG").strip())
    print("created client", flush=True)
    write_api = client.write_api(write_options=SYNCHRONOUS)
    print("write_api", flush=True)
    query_api = client.query_api()
    print("query_api", flush=True)

    while(1):
        ethId = int.from_bytes(conn.recv(1), "little")
        length = int.from_bytes(conn.recv(1), "little")
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
            IMUparse(array, client, write_api, query_api)
        elif ethId == 2:
            print(f"ID: GPS")
            GPSparse(array, client, write_api, query_api)
        elif ethId == 3:
            print(f"ID: CAN")
            CANparse(array, client, write_api, query_api)


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