from influxdb_client import Point
import logging

def GPSparse(data):

    data = ['0' if i == 0 else chr(i) for i in data]
    # logging.debug(data)

    #lat and lon is recognized by influxdb in order to show gui with map
    #converting GPS input to decimal degrees is required
    gps = { 'Status':       lambda i: i[9],
            'lat':          lambda i: (float(i[10:12]) + float(i[12:19])/60) * (-1 if i[19] == 'S' else 1), 
            'lon':          lambda i: (float(i[20:23]) + float(i[23:30])/60) * (-1 if i[30] == 'W' else 1),
            'MPH':          lambda i: float(i[31:38]) * 1.15078
    }
    for key in gps:
            logging.debug(str(key) + ": " + str(gps[key](''.join(data))))
    logging.debug("\n")
    return [Point("GPS").field(key, gps[key](''.join(data))) for key in gps]
