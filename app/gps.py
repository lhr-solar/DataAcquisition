from influxdb_client import Point
import logging

def GPSparse(data):

    data = ['0' if i == 0 else chr(i) for i in data]
    #logging.debug(data)

    gps = { 'Status':      lambda i: i[9],
            'lat':    lambda i: (float(i[10:12]) + float(i[12:18])/600000) * (-1 if i[28] == 'W' else 1), 
            'lon':   lambda i: (float(i[19:22]) + float(i[22:28])/600000) * (-1 if i[18] == 'S' else 1),
            'MPH':         lambda i: float(i[30:34]) * 1.15078
    }

    return [Point("GPS").field(key, gps[key](''.join(data))) for key in gps]

# def GPSparse(input: list):

#     gps_data = [    # GPS data string formats
#         # ['Field Name', 
#         #   Start index, 
#         #   End index (exclusive), 
#         #   Function to convert to correct format or None if no conversion needed]
#         ['Time', 0, 9, None],                                                   # Time String 'HHMMSSsss' (H: Hour, M: Minute, S: Second, s: Millisecond)
#         ['Status', 9, 10, None],                                                # A/V for Valid/Not Valid
#         ['lat', 10, 18, lambda s: float(s[0:2])+(float(s[2:])/600000.)],   # In Degrees + Minutes (DDMMMMMM -> DD MM.MMMM)
#         ['NorthSouth', 18, 19, None],                                           # N/S
#         ['lon', 19, 28, lambda s: float(s[0:3])+(float(s[3:])/600000.)],  # In Degrees + Minutes (DDDMMMMMM -> DDD MM.MMMM)
#         ['EastWest', 28, 29, None],                                             # E/W
#         ['MPH', 29, 33, lambda s: float(s)*1.15078]                             # Incoming speed in Knots
#     ]

#     input_str = ''.join([chr(c) for c in input]).replace('\x00', '0')

#     logging.debug(input_str)
#     return [Point('GPS').field(g[0], g[3](input_str[g[1]:g[2]]) if g[3] else input_str[g[1]:g[2]]) for g in gps_data[1:]]
