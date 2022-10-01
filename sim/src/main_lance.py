import logging
import socket
import time
import struct
import random

def float_func(load):
    return struct.unpack('<If', load[0:8]) + (0,)

def unsigned_func(load):
    return struct.unpack('<IQ', load[0:12]) + (0,)

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


def generate(key):
    ID = key
    IDX = struct.pack('<I', 0).ljust(4, b'\x00')
    name = CANIDs[key][0]
    func = CANIDs[key][-1]
    data = None
    if func == unsigned_func:
        data = random.randint(0, 2**31)
    elif func == float_func:
        data = random.uniform(0, 2**31)
    elif func == index_func:
        data = random.randint(0, 2**8)
    elif func == two_word_func:
        data = (random.randint(0, 2**31), random.randint(0, 2**31))

    # convert data to bytes array
    if data is not None:
        if type(data) is tuple:
            data = struct.pack('>II', *data)
        else:
            if type(data) is float:
                data = struct.pack('>f', data)
            else:
                data = struct.pack('>I', data)
    data = data.ljust(8, b'\x00')
    ID = struct.pack('>I', ID).ljust(4, b'\x00')
    data = ID + IDX + data

    return data


# testData = list(map(generate, CANIDs.keys()))

#                0123456789012345678901234567890123456789012345678901
GPS_Test_Data = "064951000A2307.1256N12016.4438E0.03165.482604063.05W"

IMU_Test_Data = [
    bytearray(b'\xf8\xfe\x01\x00\xbe\x03\x82\xfc\xaa\xfe\xcc\xfc\x00\x00\xfe\xff\x02\x00'),
    bytearray(b'\xf9\xfe\x00\x00\xbb\x03\x82\xfc\xaa\xfe\xcc\xfc\xfb\xff\xff\xff\x06\x00'),
    bytearray(b'\xfa\xfe\x01\x00\xbe\x03\x82\xfc\xaa\xfe\xcc\xfc\xf3\xff\xfa\xff\x0b\x00')
]

# the different componenes of GPS data, first element is idk, then lat big, lat small, N or S
# long big, long small, W or E, mph, unknown
GPS_Test_Data_array = ["064951000A", 2307, ".", 1256, "N", 12016, ".", 4438, "E", 0.03165, ".482604063.05W"]

HOST = 'app'
PORT = 65432

def send_data(CAN, index, socket):
    index = list(map(lambda e: int(e), index))
    socket.send(bytearray(CAN + index[3::-1] + index[7:3:-1] + index[16:7:-1]))

#This is the only function that should be called outside of this file. Other functions will be called within this function
def sender():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    logging.debug("Client starting...")
    s.setblocking(True)
    eth_header_CAN = [0x03, 0x10]
    eth_header_GPS = [0x02, len(GPS_Test_Data)]
    eth_header_IMU = [0x01, 0x12]

    while True:
        testData = list(map(generate, CANIDs.keys()))
        s.sendall(bytearray(eth_header_GPS) + GPS_Test_Data.encode())
        #logging.debug("GPS sent.")
        for i in IMU_Test_Data:
            s.sendall(bytearray(eth_header_IMU) + i)
        for data in testData:
            send_data(eth_header_CAN, data, s)
        time.sleep(.5)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    sender()
    # HOST = 'localhost'
    # PORT = 65432