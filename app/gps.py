from influxdb_client import Point
import logging


def GPSparse(data):
    #TODO: Parse NMEA Sentence
    logging.debug(data)
    logging.debug("\n")
