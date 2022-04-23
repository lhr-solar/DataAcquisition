from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import asyncio
import os

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

async def CANparse(canArray):
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
    await asyncio.sleep(.2)