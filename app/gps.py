from influxdb_client import Point
import logging

def GPSparse(data):

    logging.debug(data)

    gps = [ ["Status",      data[9]]
            ["Latitude",    float(data[10:11]) + float(data[11:18])/600000] 
            ["NorthSouth",  data[18]] 
            ["Longitude",   float(data[19:22]) + float(data[22:28])/600000]
            ["EastWest",    data[29]]
            ["MPH",         float(data[30:33]) * 1.15078]
    ]

    return [Point("GPS").field((gps[i][0], gps[i][1]) for i in gps)]
