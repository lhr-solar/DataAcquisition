from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import os
import asyncio

async def IMUparse(array):
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
    while True:
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
        await asyncio.sleep(.2)

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

@app.on_event("startup")
async def on_startup():
    asyncio.create_task(IMUparse(array)) 


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    ip = os.environ.get("PI_IP")
    return templates.TemplateResponse("index.html", {"request": request, "ip": ip})

