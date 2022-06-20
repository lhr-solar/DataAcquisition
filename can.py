import struct
from functools import partial

def float_func(load):
    return struct.unpack('f', load[0:4])

def unsigned_func(load, length):
    return struct.unpack('B', load[0: length])

def two_word_func(load):
    return (struct.unpack('B', load[0:4]), struct.unpack('B', load[4:8]))

def index_func(load):
    return (struct.unpack('B', load[0:1]), struct.unpack('B', load[1:5]))

CANIDs = {
    0x001: ["Dash Kill Switch",                             partial(unsigned_func, length=1)],
    0x002: ["BPS Trip",                                     partial(unsigned_func, length=1)],
    0x003: ["Any System Failures",                          partial(unsigned_func, length=1)],
    0x004: ["Ignition",                                     partial(unsigned_func, length=1)],
    0x005: ["Any System Shutoff",                           partial(unsigned_func, length=1)],

    0x101: ["BPS All Clear",                                partial(unsigned_func, length=1)],
    0x102: ["BPS Contactor State",                          partial(unsigned_func, length=1)],
    0x103: ["Current Data",                                 partial(unsigned_func, length=4)],
    0x104: ["Voltage Data Array",                           index_func],
    0x105: ["Temperature Data Array",                       index_func],
    0x106: ["State of Charge Data",                         partial(unsigned_func, length=4)],
    0x107: ["WDog Triggered",                               partial(unsigned_func, length=1)],
    0x108: ["CAN Error",                                    partial(unsigned_func, length=1)],
    0x109: ["BPS Command msg",                              partial(unsigned_func, length=8)],
    0x10B: ["Supplemental Voltage",                         partial(unsigned_func, length=2)],
    0x10C: ["Charging Enabled",                             partial(unsigned_func, length=1)],

    0x580: ["Car State",                                    partial(unsigned_func, length=1)],
    0x242: ["Motor Controller Bus",                         two_word_func],
    0x243: ["Velocity",                                     two_word_func],
    0x244: ["Motor Controller Phase Current",               two_word_func],
    0x245: ["Motor Voltage Vector",                         two_word_func],
    0x246: ["Motor Current Vector",                         two_word_func],
    0x247: ["Motor BackEMF",                                two_word_func],
    0x24B: ["Motor Temperature",                            two_word_func],
    0x24E: ["Odometer & Bus Amp Hours",                     two_word_func],
    0x24F: ["Array Contactor State Change",                 partial(unsigned_func, length=1)],

    0x600: ["Sunscatter A Array Voltage Setpoint",          float_func],
    0x601: ["Sunscatter A Array Voltage Measurement",       float_func],
    0x602: ["Sunscatter A Array Current Measurement",       float_func],
    0x603: ["Sunscatter A Battery Voltage Measurement",     float_func],
    0x604: ["Sunscatter A Battery Current Measurement",     float_func],
    0x605: ["Sunscatter A Override Enabled/Disable command", partial(unsigned_func, length=1)],
    0x606: ["Sunscatter A Fault",                           partial(unsigned_func, length=1)],
    0x610: ["Sunscatter B Array Voltage Setpoint",          float_func],
    0x611: ["Sunscatter B Array Voltage Measurement",       float_func],
    0x612: ["Sunscatter B Array Current Measurement",       float_func],
    0x613: ["Sunscatter B Battery Voltage Measurement",     float_func],
    0x614: ["Sunscatter B Battery Current Measurement",     float_func],
    0x615: ["Sunscatter B Override Enabled/Disable command", partial(unsigned_func, length=1)],
    0x616: ["Sunscatter B Fault",                           partial(unsigned_func, length=1)],

    0x620: ["Blackbody Measurement",                        index_func],
    0x630: ["Blackbody (Irradiance Sensor 1) Measurement",  float_func],
    0x631: ["Blackbody (Irradience Sensor 2) Measurement",  float_func],
    0x632: ["Blackbody (Irradience/RTD) Board Enabled/Disable command", partial(unsigned_func, length=1)],
    0x633: ["Blackbody (Irradience/RTD) Board Fault", partial(unsigned_func, length=1)],
    0x640: ["PV Curve Tracer Profile", partial(unsigned_func, length=1)]
}

def CANparse(canArray):
    canID = int.from_bytes(canArray[0:4], "little")
    print(CANIDs[canID][1](load=canArray[4:12]))