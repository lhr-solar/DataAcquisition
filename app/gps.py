from influxdb_client import Point
from influxdb_client.client.write_api import SYNCHRONOUS
import logging

def GPSparse(data):
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

    logging.debug(data)
    
    r = []

    # g1 = Point("hr").field(hr)
    # g2 = Point("min").field(min)
    # g3 = Point("ms").field(ms)
    g4 = Point("GPS").field("latitute_Deg", latitude_Deg)
    g5 = Point("GPS").field("latitude_Min", latitude_Min)
    g6 = Point("GPS").field("NorthSouth", NorthSouth)
    g7 = Point("GPS").field("longitude_Deg", longitude_Deg)
    g8 = Point("GPS").field("longitude_Min", longitude_Min)
    g9 = Point("GPS").field("EastWest", EastWest)
    g10 = Point("GPS").field("speedInKnots", speedInKnots)
    # g11 = Point("day").field(day)
    # g12 = Point("year").field(year)
    # g13 = Point("month").field(month)
    # g14 = Point("magneticVariation_Deg").field(magneticVariation_Deg)
    # g15 = Point("magneticVariation_EastWest").field(magneticVariation_EastWest)
    
    r += [g4, g5, g6, g7, g8, g9, g10]
        
    return r
