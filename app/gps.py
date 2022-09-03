from influxdb_client import Point
import logging

def GPSparse(data):

    data = ['0' if i == 0 else chr(i) for i in data]
    logging.debug(data)

    #lat and lon is recognized by influxdb in order to show gui with map
    #converting GPS input to decimal degrees is required
    gps = { 'Status':       lambda i: i[9],
            'lat':          lambda i: (float(i[10:14]) + float(i[15:19])/600000) * (-1 if i[30] == 'W' else 1), 
            'lon':          lambda i: (float(i[20:25]) + float(i[26:30])/600000) * (-1 if i[19] == 'S' else 1),
            'MPH':          lambda i: float(i[31:38]) * 1.15078
    }
    for key in gps:
        logging.debug(key)
        logging.debug(gps[key](''.join(data)))
    return [Point("GPS").field(key, gps[key](''.join(data))) for key in gps]
