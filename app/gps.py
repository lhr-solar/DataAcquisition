from influxdb_client import Point
from influxdb_client.client.write_api import SYNCHRONOUS
import logging

def GPSparse(data):

    logging.debug(data)
    
    r = []

    g3 = Point("GPS").field("Status", data[9])
    g4 = Point("GPS").field("Latitute", data[10:18])
    g6 = Point("GPS").field("NorthSouth", data[18])
    g7 = Point("GPS").field("Longitude", data[19:28])  #may need to reverse all lists since little endian
    g9 = Point("GPS").field("EastWest", data[29])
    g10 = Point("GPS").field("MPH", str(ord(data[30]) + (int(data[32:30:-1]) / 100)  * 1.15078)) #convert knots in char to mph in char
    
    r += [g3, g4, g6, g7, g9, g10]
        
    return r
