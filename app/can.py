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

def signed_float_func(load):
    return struct.unpack('<If', load[0:12]) + (0,)

def index_func(load):
    return struct.unpack('<II', load[0:8]) + (0,)

def two_word_func(load):
    return struct.unpack('<III', load[0:12])

def word_byte_func(load):
    return struct.unpack('<IHB', load[0:12]) + (0,)

def signedWord_byte_func(load):
    return struct.unpack('<IfB', load[0:12]) + (0,)

def processTwoAndOneBytes(load):
    return struct.unpack('<IHB', load[0:8]) + (0,)

def processFourAndOneByte(load):
    return struct.unpack('<IIB', load[0:12]) + (0,)

def signed_float_two_word_func(load):
    return struct.unpack('<Iff', load[0:12]) + (0,)

def four_byte_func(load):
    return struct.unpack('<IBBBB', load[0:8]) + (0,)

def sunScatterSensorConfigure(load):
    return struct.unpack('<IHBBB', load[0:12]) + (0,)

def motor_status_func(load):
    idx = struct.unpack('<I', load[0:4])
    limit_flags = [int(i) for i in bin(int.from_bytes(load[4:6], byteorder='little', signed=False))[2:]]
    limit_flags = limit_flags[0:7]
    error_flags = [int(i) for i in bin(int.from_bytes(load[6:8], byteorder='little', signed=False))[2:]]
    error_flags = error_flags[0:9]
    data = struct.unpack('<HBB', load[8:12])
    return idx + tuple(limit_flags) + tuple(error_flags) + tuple(data)



CANIDs = {
    0x001: ["Dash Kill Switch",                                 unsigned_func],
    0x002: ["BPS Trip",                                         unsigned_func],
    0x003: ["Any System Failures",                              unsigned_func],
    0x004: ["Ignition",                                         unsigned_func],
    0x005: ["Any System Shutoff",                               unsigned_func],

    0x101: ["BPS All Clear",                                    unsigned_func],
    0x102: ["BPS Contactor State",                              unsigned_func],
    0x103: ["Current Data",                                     fixed_func],  # was signed_func before
    0x104: ["Voltage Data Array",                               index_func],
    0x105: ["Temperature Data Array",                           index_func],
    0x106: ["State of Charge Data",                             fixed_func],  # used to be unsigned 
    0x107: ["WDog Triggered",                                   unsigned_func],
    0x108: ["CAN Error",                                        unsigned_func],
    0x109: ["BPS Command msg",                                  unsigned_func],
    0x10B: ["Supplemental Voltage",                             unsigned_func],
    0x10C: ["Charging Enabled",                                 unsigned_func], 

    0x580: ["CONTROL_MODE",                                     unsigned_func],    
    0x581: ["IO_STATE", "Accel Pedal", "Brake Pedal",
            "Switch Bitmap", "Contactor Bitmap",                four_byte_func],
    0x240: ["Motor Controller Identification", "Prohelion ID",
            "Device serial number",                             two_word_func], # Device sereial number is [32 : 63] but should be [63 : 32]? or doesn't matter
    0x241: ["Motor Status", "Output Voltage PWM",
            "Motor Current", "Velocity", "Bus Current",
            "Bus Voltage Upper Limit", "Bus Voltage Lower Limit",
            "IPM or Motor Temperature",
            "Hardware over current",
            "Software over current", "DC Bus over voltage",
            "Bad motor position hall sequence",
            "Watchdog caused last reset", "Config read error",
            "15V rail under voltage lock out",
            "Desaturation fault", "Motor Over Speed",
            "Active Motor index",
            "Transmit error count", "Receive error count",      motor_status_func],
    0x242: ["Motor Controller Bus", "Voltage", "Current",       two_word_func],
    0x243: ["Velocity", "rpm", "m/s",                           two_word_func], 
    0x244: ["Motor Controller Phase Current", "B", "C",         two_word_func],
    0x245: ["Motor Voltage Vector", "Imaginary", "Real",        two_word_func],
    0x246: ["Motor Current Vector", "Imaginary", "Real",        two_word_func], 
    0x247: ["Motor BackEMF", "Phase Peak", "Real",              two_word_func], 
    0x248: ["15V Voltage Rail", "Reserved", "Actual Voltage",              two_word_func], # reserved not a field?
    0x249: ["3.3V and 1.9V Voltage Rail Measurement", 
            "Actual 1.9V DSP Power Rail Voltage", 
            "Actal 3.3V rail voltage",                          two_word_func], 
    0x24B: ["Motor Temperature", "Internal motor temp", 
            "Internal heat-sink temp",                          two_word_func], 
    # 0x24B: ["Motor Temperature", "Phase C", "Internal",         two_word_func], # other 2 fields don't match table
    0x24C: ["DSP Board Temperature", "DSP board temp" , "Reserved",     two_word_func], # reserved not given a field?
    # 0x24E: ["Odometer & Bus Amp Hours", "Charge", "Distance",   two_word_func], 
    0x24E: ["Odometer & Bus Amp Hours", "Distance travelled since reset", 
            "Charge flow into controller DC bus from reset",    two_word_func], 
    0x257: ["Slip Speed Measurement", "Distance", "Slip speed", two_word_func],
    0x24F: ["Array Contactor State Change",                     unsigned_func], 

    0x600: ["Sunscatter A Heartbeat",                           unsigned_func],
    0x601: ["Sunscatter A Set Mode; BOARD OVERRIDE ENABLE/DISABLE", unsigned_func],
    0x602: ["Sunscatter A Board Fault",                         unsigned_func],
    0x603: ["Sunscatter A Acknowledge Fault",                   unsigned_func],
    0x604: ["Sunscatter A Sensor Configure",                    sunScatterSensorConfigure],
    0x605: ["Sunscatter A Sensor Configure 2",                  signedWord_byte_func],
    0x606: ["Sunscatter A Sensor Configure 3",                  signedWord_byte_func],
    0x608: ["Sunscatter A Debug Configure",                     unsigned_func],
    0x609: ["Sunscatter A Operating Setpoint",                  signed_float_two_word_func], 
    0x60A: ["Sunscatter A Input Voltage Measurement",           signed_float_func], 
    0x60B: ["Sunscatter A Input Current Measurement",           signed_float_func],
    0x60C: ["Sunscatter A Output Voltage Measurement",          signed_float_func], 
    0x60D: ["Sunscatter A Output Current Measurement",          signed_float_func],
    

    0x610: ["Sunscatter B Heartbeat",                           unsigned_func],
    0x611: ["Sunscatter B Set Mode; BOARD OVERRIDE ENABLE/DISABLE", unsigned_func],
    0x612: ["Sunscatter B Board Fault",                         unsigned_func],
    0x613: ["Sunscatter B Acknowledge Fault",                   unsigned_func],
    0x614: ["Sunscatter B Sensor Configure",                    sunScatterSensorConfigure],
    0x615: ["Sunscatter B Sensor Configure 2",                  signedWord_byte_func],
    0x616: ["Sunscatter B Sensor Configure 3",                  signedWord_byte_func],
    0x618: ["Sunscatter B Debug Configure",                     unsigned_func],
    0x619: ["Sunscatter B Operating Setpoint",                  signed_float_two_word_func], 
    0x61A: ["Sunscatter B Input Voltage Measurement",           signed_float_func], 
    0x61B: ["Sunscatter B Input Current Measurement",           signed_float_func],
    0x61C: ["Sunscatter B Output Voltage Measurement",          signed_float_func], 
    0x61D: ["Sunscatter B Output Current Measurement",          signed_float_func], 

    0x620: ["Sunscatter C Heartbeat",                           unsigned_func],
    0x621: ["Sunscatter C Set Mode; BOARD OVERRIDE ENABLE/DISABLE", unsigned_func],
    0x622: ["Sunscatter C Board Fault",                         unsigned_func],
    0x623: ["Sunscatter C Acknowledge Fault",                   unsigned_func],
    0x624: ["Sunscatter C Sensor Configure",                    sunScatterSensorConfigure],
    0x625: ["Sunscatter C Sensor Configure 2",                  signedWord_byte_func],
    0x626: ["Sunscatter C Sensor Configure 3",                  signedWord_byte_func],
    0x628: ["Sunscatter C Debug Configure",                     unsigned_func],
    0x629: ["Sunscatter C Operating Setpoint",                  signed_float_two_word_func], 
    0x62A: ["Sunscatter C Input Voltage Measurement",           signed_float_func], 
    0x62B: ["Sunscatter C Input Current Measurement",           signed_float_func],
    0x62C: ["Sunscatter C Output Voltage Measurement",          signed_float_func], 
    0x62D: ["Sunscatter C Output Current Measurement",          signed_float_func], 

    0x650: ["Blackbody A Heartbeat",                            unsigned_func],
    0x651: ["Blackbody A Set Mode",                             unsigned_func],
    0x652: ["Blackbody A Board Fault",                          unsigned_func],
    0x653: ["Blackbody A Acknowledge Fault",                    unsigned_func],
    0x654: ["Blackbody A Temperature Sensor Configure",         word_byte_func],
    0x655: ["Blackbody A Irradiance Sensor Configure",          word_byte_func], 
    0x656: ["Blackbody A Temperature Measurement",              signedWord_byte_func],
    0x657: ["Blackbody A Irradiance Measurement",               signedWord_byte_func],

}


def CANparse(data):
    
    logging.debug(data)
    canID = int.from_bytes(data[0:4], "little")
    logging.debug(canID)
    packet = CANIDs[canID][-1](data[4:])
    canIdFunction = CANIDs[canID][-1]
    
    twoFieldFunctions = [two_word_func, word_byte_func, signedWord_byte_func, processTwoAndOneBytes, processFourAndOneByte, signed_float_two_word_func]
    fourFieldFunctions = [four_byte_func, sunScatterSensorConfigure]

    if (canIdFunction in twoFieldFunctions):
        for i in range(1,3):
            logging.debug(CANIDs[canID][0] + "->" + CANIDs[canID][i] + ": " + str(packet[i]))
        return [Point(CANIDs[canID][0]).field(CANIDs[canID][i], packet[i]) #return data type and data for both data fields
            for i in [1,2]]
    
    elif (canIdFunction in fourFieldFunctions):
        for i in range(1,5):
            logging.debug(CANIDs[canID][0] + "->" + CANIDs[canID][i] + ": " + str(packet[i]))
        return [Point(CANIDs[canID][0]).field(CANIDs[canID][i], packet[i]) #return data type and data for both data fields
            for i in [1,2,3,4]]
    
    elif(canIdFunction == motor_status_func):
        for i in range(1, 20):
            logging.debug(CANIDs[canID][0] + "->" + CANIDs[canID][i] + ": " + str(packet[i]))
        return [Point(CANIDs[canID][0]).field(CANIDs[canID][i], packet[i]) #return data type and data for both data fields
            for i in range(1, 20)]
    
    else:
        logging.debug(CANIDs[canID][0] + ": " + str(packet[1]) + "\n")
        return Point(CANIDs[canID][0]).field(packet[0], packet[1]) #return just index and data


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    #i = [0x00, 0x00, 0x05, 0x81, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x03, 0xFF, 0xFF, 0xFF] #IO_STATE
    i = [0x00, 0x00, 0x02, 0x41, 0x00, 0x00, 0x00, 0x00, 0x80, 0x80, 0x80, 0x00, 0xFF, 0xFF, 0xFF, 0xFF] #Motor Controller Bus 12V 100A
    
    canID = i[3::-1]
    idx = i[7:3:-1]
    data = i[16:7:-1]
    # print("data: ", bytearray(data))
    print(bin(int.from_bytes(bytearray(data))))
    canSend = bytearray(canID + idx + data)
    print(CANparse(canSend))