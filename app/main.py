from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import os
import random
import asyncio

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

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

@app.on_event("startup")
async def on_startup():
    asyncio.create_task(tester()) 


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    ip = os.environ.get("PI_IP")
    return templates.TemplateResponse("index.html", {"request": request, "ip": ip})
