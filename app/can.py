import struct
import logging
from influxdb_client import Point

def float_func(load):
    return struct.unpack('<If', load[0:8]) + (0,)

def fixed_func(load):
    unpacked = struct.unpack('<Iq', load[0:12])
    unpacked_list = list(unpacked)
    unpacked_list[1] /= 1000000
    return tuple(unpacked_list) + (0,)

def unsigned_func(load):
    return struct.unpack('<IQ', load[0:12]) + (0,)

def signed_func(load):
    return struct.unpack('<Ii', load[0:8]) + (0,)

def two_word_func(load):
    return struct.unpack('<III', load[0:12])

def index_func(load):
    return struct.unpack('<II', load[0:8]) + (0,)

CANIDs = {
    0x001: ["Dash Kill Switch",                                 unsigned_func],
    0x002: ["BPS Trip",                                         unsigned_func],
    0x003: ["Any System Failures",                              unsigned_func],
    0x004: ["Ignition",                                         unsigned_func],
    0x005: ["Any System Shutoff",                               unsigned_func],

    0x101: ["BPS All Clear",                                    unsigned_func],
    0x102: ["BPS Contactor State",                              unsigned_func],
    0x103: ["Current Data",                                     signed_func],       #used to be unsigned
    0x104: ["Voltage Data Array",                               index_func],
    0x105: ["Temperature Data Array",                           index_func],
    0x106: ["State of Charge Data",                             fixed_func],        #used to be unsigned 
    0x107: ["WDog Triggered",                                   unsigned_func],
    0x108: ["CAN Error",                                        unsigned_func],
    0x109: ["BPS Command msg",                                  unsigned_func],
    0x10B: ["Supplemental Voltage",                             unsigned_func],
    0x10C: ["Charging Enabled",                                 unsigned_func],

    0x580: ["Car State",                                        unsigned_func],     #not used
    0x242: ["Motor Controller Bus", "Current", "Voltage",       two_word_func],
    0x243: ["Velocity", "m/s", "rpm",                           two_word_func],
    0x244: ["Motor Controller Phase Current", "B", "C",         two_word_func],
    0x245: ["Motor Voltage Vector", "Real", "Imaginary",        two_word_func],
    0x246: ["Motor Current Vector", "Real", "Imaginary",        two_word_func],
    0x247: ["Motor BackEMF", "Real", "Phase Peak",              two_word_func],
    0x24B: ["Motor Temperature", "Phase C", "Internal",         two_word_func],
    0x24E: ["Odometer & Bus Amp Hours", "Charge", "Distance",   two_word_func],
    0x24F: ["Array Contactor State Change",                     unsigned_func],

    0x600: ["Sunscatter A Array Voltage Setpoint",              float_func],
    0x601: ["Sunscatter A Array Voltage Measurement",           float_func],
    0x602: ["Sunscatter A Array Current Measurement",           float_func],
    0x603: ["Sunscatter A Battery Voltage Measurement",         float_func],
    0x604: ["Sunscatter A Battery Current Measurement",         float_func],
    0x605: ["Sunscatter A Override command",                    unsigned_func],
    0x606: ["Sunscatter A Fault",                               unsigned_func],
    0x610: ["Sunscatter B Array Voltage Setpoint",              float_func],
    0x611: ["Sunscatter B Array Voltage Measurement",           float_func],
    0x612: ["Sunscatter B Array Current Measurement",           float_func],
    0x613: ["Sunscatter B Battery Voltage Measurement",         float_func],
    0x614: ["Sunscatter B Battery Current Measurement",         float_func],
    0x615: ["Sunscatter B Override command",                    unsigned_func],
    0x616: ["Sunscatter B Fault",                               unsigned_func],

    0x620: ["Blackbody Measurement",                            index_func],
    0x630: ["Blackbody 1 Measurement",                          float_func],
    0x631: ["Blackbody 2 Measurement",                          float_func],
    0x632: ["Blackbody Board command",                          unsigned_func],
    0x633: ["Blackbody Board Fault",                            unsigned_func],
    0x640: ["PV Curve Tracer Profile",                          unsigned_func]
}

def CANparse(data):
    logging.debug(data)
    canID = int.from_bytes(data[0:4], "little")
    logging.debug(canID)
    packet = CANIDs[canID][-1](data[4:])
    logging.debug(CANIDs[canID][0])
    logging.debug(packet[1])

    return (Point(CANIDs[canID][0]).field(packet[0], packet[1]) #return just index and data
            if (packet[2] == 0) 
            else 
                [Point(CANIDs[canID][0]).field(CANIDs[canID][i], packet[i]) #return data type and data for both data fields
                for i in [1,2]] 
            )
