from influxdb_client import Point
import logging

def GPSparse(data):

    data = ['0' if i == 0 else chr(i) for i in data]
    logging.debug(data)

    #lat and lon is recognized by influxdb in order to show gui with map
    #converting GPS input to decimal degrees is required
    gps = { 'Status':       lambda i: i[9],
            'lat':          lambda i: (float(i[10:12]) + float(i[12:18])/600000) * (-1 if i[28] == 'W' else 1), 
            'lon':          lambda i: (float(i[19:22]) + float(i[22:28])/600000) * (-1 if i[18] == 'S' else 1),
            'MPH':          lambda i: float(i[30:34]) * 1.15078
    }

    return [Point("GPS").field(key, gps[key](''.join(data))) for key in gps]
