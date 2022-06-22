import struct
import logging
from influxdb_client import Point

def float_func(load):
    return [0, struct.unpack('<f', load[0:4])[0], 0]

def unsigned_func(load):
    logging.debug(load)
    return [0, struct.unpack('<Q', load)[0], 0]

def two_word_func(load):
    return [0, struct.unpack('<I', load[0:4])[0], struct.unpack('<I', load[4:8])[0]]

def index_func(load):
    return [struct.unpack('<I', load[0:4])[0], struct.unpack('<I', load[4:8])[0], 0]

CANIDs = {
    0x001: ["Dash Kill Switch",                                 unsigned_func],
    0x002: ["BPS Trip",                                         unsigned_func],
    0x003: ["Any System Failures",                              unsigned_func],
    0x004: ["Ignition",                                         unsigned_func],
    0x005: ["Any System Shutoff",                               unsigned_func],

    0x101: ["BPS All Clear",                                    unsigned_func],
    0x102: ["BPS Contactor State",                              unsigned_func],
    0x103: ["Current Data",                                     unsigned_func],
    0x104: ["Voltage Data Array",                               index_func],
    0x105: ["Temperature Data Array",                           index_func],
    0x106: ["State of Charge Data",                             unsigned_func],
    0x107: ["WDog Triggered",                                   unsigned_func],
    0x108: ["CAN Error",                                        unsigned_func],
    0x109: ["BPS Command msg",                                  unsigned_func],
    0x10B: ["Supplemental Voltage",                             unsigned_func],
    0x10C: ["Charging Enabled",                                 unsigned_func],

    0x580: ["Car State",                                        unsigned_func],
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
    logging.debug(CANIDs[canID][0])
    packet = CANIDs[canID][-1](data[4:12])
    logging.debug(packet)

    return (Point(CANIDs[canID][0]).field(packet[0], packet[1]) 
            if (packet[2] == 0) 
            else 
                [Point(CANIDs[canID][0]).field(CANIDs[canID][i], packet[i])
                for i in [1,2]] 
            )
