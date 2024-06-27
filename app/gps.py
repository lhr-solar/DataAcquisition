from influxdb_client import Point
import logging


def GPSparse(data):
    #TODO: Parse NMEA Sentence
    # Could not Conclude that data size is constant
    # Therefore had to sperate based on comma characters 
    data_str = data.decode('utf-8')
    info_list = data_str.split(',')

    # If the data the type we want and is valid, log it 
    if(info_list[0] == "GNRMC" and info_list[2] == "A"):
   
        #lat and lon is recognized by influxdb in order to show gui with map
        #converting GPS input to decimal degrees is required
        gps = { 'Status':       float(1), 
                'lat':          (float(info_list[3]) / 100.0) * (-1 if info_list[4] == 'S' else 1), 
                'lon':          (float(info_list[5]) / 100.0) * (-1 if info_list[6] == 'W' else 1), 
                'MPH':          (float(info_list[7]) * 1.15078), # Data is in Knots / Hour, Have to convert Knots --> Miles 
        }
        for key in gps:
            logging.debug(str(key) + ": " + str(gps[key]))
        logging.debug("\n")
        return [Point("GPS").field(key, gps[key]) for key in gps]
