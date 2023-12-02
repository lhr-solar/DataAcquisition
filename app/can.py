import struct
import logging
from influxdb_client import Point


def float_func(load):
    print(struct.unpack('<If', load[0:8]) + (0,))
    return struct.unpack('<If', load[0:8]) + (0,)

def fixed_func(load):
    unpacked = struct.unpack('<Iq', load[0:12])
    unpacked_list = list(unpacked)
    print(unpacked_list)
    unpacked_list[1] /= 1000000
    print(tuple(unpacked_list) + (0,))
    return tuple(unpacked_list) + (0,)


def unsigned_func(load):
    return struct.unpack('<IQ', load[0:12]) + (0,)

def signed_func(load):
    return struct.unpack('<Ii', load[0:8]) + (0,)

def two_word_func(load):
    return struct.unpack('<III', load[0:12])

def index_func(load):
    print(struct.unpack('<II', load[0:8]) + (0,))
    return struct.unpack('<II', load[0:8]) + (0,)

def four_byte_func(load):
    return struct.unpack('<IBBBB', load[0:8]) + (0,)

def motor_status_func(load):
    idx = struct.unpack('<I', load[0:4])
    print("idx:", idx)
    limit_flags =   [int(bit) for byte in load[4:6] for bit in f"{byte:08b}"[::-1]]
    limit_flags = limit_flags[0:7] # Only take the first 7 b/c bit[7] to bit [15] are reserved (not used now)
    error_flags = [int(bit) for byte in load[6:8] for bit in f"{byte:08b}"[::-1]] 
    error_flags = error_flags[0:9] # Only take the first 9 b/c bit[25] to bit [31] are reserved (not used now)
    data = struct.unpack('<HBB', load[8:12])
    return idx + tuple(limit_flags) + tuple(error_flags) + tuple(data)

def processTwoAndOneBytes(load):
    return struct.unpack('<IHB', load[0:7]) # is [0:7] correct?

def processFourAndOneByte(load):
    return struct.unpack('<IIB', load[0:9]) # is [0:9] correct?

def PV_Curve_Tracer_Profile_func(load):
     # TODO: This function is unfinished and will not return a correct value. I processed test regieme incorrectly (I didn't identify bits 24, 25, 26 correctly) and did not get to test ID

    idx = struct.unpack('<I', load[0:4])
    first = struct.unpack('<BBB', load[4:7])

    test_regieme = bin(int.from_bytes(load[7:8], byteorder='little', signed=False))[2:]
    test_regieme = list(test_regieme)

    if len(test_regieme) != 8:
        test_regieme = [0] * (8 - len(test_regieme)) + test_regieme

    test_regieme = test_regieme[0:3] # processed this incorrectly.  


    testID = bin(int.from_bytes(load[7:9], byteorder='little', signed=False))[2:]

    return idx + first + tuple(test_regieme) + tuple()

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

    0x580: ["CONTROL_MODE",                                     unsigned_func],     # need custom
    0x581: ["IO_STATE", "Accel Pedal", "Brake Pedal",
            "Switch Bitmap", "Contactor Bitmap",                four_byte_func],
    0x240: ["Motor Controller Identification", "Prohelion ID",
            "Device serial number",                             two_word_func],
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
    0x243: ["Velocity", "rpm", "m/s",                           two_word_func], # swapped fields to correct order
    0x244: ["Motor Controller Phase Current", "B", "C",         two_word_func],
    0x245: ["Motor Voltage Vector", "Imaginary", "Real",        two_word_func], # swapped fields to correct order
    0x246: ["Motor Current Vector", "Imaginary", "Real",        two_word_func], # swapped fields to correct order
    0x247: ["Motor BackEMF", "Phase Peak", "Real",              two_word_func], # swapped fields to correct order
    0x248: ["15V Voltage Rail",  "Actual Voltage",              two_word_func], 
    0x249: ["3.3V and 1.9V Voltage Rail Measurement", 
            "Actual 1.9V DSP Power Rail Voltage", 
            "Actal 3.3V rail voltage",                          two_word_func], # added
    0x24B: ["Motor Temperature", "Internal motor temp", 
            "Internal heat-sink temp",                          two_word_func], # changed fields to match
    # 0x24B: ["Motor Temperature", "Phase C", "Internal",         two_word_func], # other 2 fields don't match table
    0x24C: ["DSP Board Temperature", "DSP board temp",          two_word_func], 
    # 0x24E: ["Odometer & Bus Amp Hours", "Charge", "Distance",   two_word_func], # changed fields to match
    0x24E: ["Odometer & Bus Amp Hours", "Distance travelled since reset", 
            "Charge flow into controller DC bus from reset",    two_word_func], 
    0x257: ["Slip Speed Measurement", "Distance", "Slip speed", two_word_func],
    0x24F: ["Array Contactor State Change",                     unsigned_func], 

    0x600: ["Sunscatter A Array Voltage Setpoint",              float_func],
    0x601: ["Sunscatter A Array Voltage Measurement",           float_func],
    0x602: ["Sunscatter A Array Current Measurement",           float_func],
    0x603: ["Sunscatter A Battery Voltage Measurement",         float_func],
    0x604: ["Sunscatter A Battery Current Measurement",         float_func],
    0x605: ["Sunscatter A Override command",                    unsigned_func], # is this func correct?
    0x606: ["Sunscatter A Fault",                               unsigned_func],
    0x610: ["Sunscatter B Array Voltage Setpoint",              float_func],
    0x611: ["Sunscatter B Array Voltage Measurement",           float_func],
    0x612: ["Sunscatter B Array Current Measurement",           float_func],
    0x613: ["Sunscatter B Battery Voltage Measurement",         float_func],
    0x614: ["Sunscatter B Battery Current Measurement",         float_func],
    0x615: ["Sunscatter B Override command",                    unsigned_func], # is this func correct?
    0x616: ["Sunscatter B Fault",                               unsigned_func],

    # 0x620: ["Blackbody RTD Sensor Measurement",                 index_func], # doesn't match - on sheet is "heartbeat". unsure what to do
    0x620: ["Heartbeat",                                        unsigned_func], 
    0x621: ["Set Mode",                                         unsigned_func], # added 
    0x622: ["Blackbody Board Fault",                            unsigned_func], # added
    0x623: ["Acknowledge Fault",                                unsigned_func], # added 
    0x624: ["RTD Configure", 
            "RTD Sample Frequency", 
            "Enabled RTDs",                                     processTwoAndOneBytes], # added #^^ need custom [23:16] [15:0] 1 2

    0x625: ["Irradiance Configure", 
            "Irradiance Sample Frequency", 
            "Enabled Irradiance Sensor",                        processTwoAndOneBytes], # added #^^ need custom [23:16] [15:0]
    0x626: ["Blackbody (RTD Sensor) Measurement", 
            "Temperature measurement", 
            "RTD ID",                                           processFourAndOneByte], # added # ^^ need custom [39:32][31:0] 1 4

    0x627: ["Blackbody Irradiance Measurement", 
            "Irradiance measurement", 
            "Irradiance Sensor ID",                             processFourAndOneByte], # added # ^^ need custom [39:32][31:0]  1  4


    0x630: ["Blackbody Irradiance Sensor 1 Measurement",        float_func], # not on sheet
    0x631: ["Blackbody Irradiance Sensor 2 Measurement",        float_func], # not on sheet
    0x632: ["Blackbody Irradiance Board command",               unsigned_func], # not on sheet
    0x633: ["Blackbody Irradiance Board Fault",                 unsigned_func], # not on sheet
    # 0x640: ["PV Curve Tracer Profile",                          unsigned_func], # needs custom function
    0x640: ["PV Curve Tracer Profile", "PWMResolution", "End PWM", "Start PWM", "Test Regime", "Test ID", PV_Curve_Tracer_Profile_func] # ^^ need custom

}


def CANparse(data):
    
    logging.debug(data)
    canID = int.from_bytes(data[0:4], "little")
    logging.debug(canID)
    packet = CANIDs[canID][-1](data[4:])
    
    if (CANIDs[canID][-1] == two_word_func):
        for i in range(1,3):
            logging.debug(CANIDs[canID][0] + "->" + CANIDs[canID][i] + ": " + str(packet[i]))
        return [Point(CANIDs[canID][0]).field(CANIDs[canID][i], packet[i]) #return data type and data for both data fields
            for i in [1,2]]
    
    elif (CANIDs[canID][-1] == four_byte_func):
        for i in range(1,5):
            logging.debug(CANIDs[canID][0] + "->" + CANIDs[canID][i] + ": " + str(packet[i]))
        return [Point(CANIDs[canID][0]).field(CANIDs[canID][i], packet[i]) #return data type and data for both data fields
            for i in [1,2,3,4]]
    
    elif(CANIDs[canID][-1] == motor_status_func):
        for i in range(1, min(20, len(CANIDs[canID]), len(packet))): # Added b/c was getting out of index error 
            logging.debug(CANIDs[canID][0] + "->" + CANIDs[canID][i] + ": " + str(packet[i]))
        return [Point(CANIDs[canID][0]).field(CANIDs[canID][i], packet[i]) #return data type and data for both data fields
            for i in range(1, min(20, len(CANIDs[canID]), len(packet)))] #Added b/c was getting out of index error 
    
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
    #print(bin(int.from_bytes(bytearray(data))))
    
    canSend = bytearray(canID + idx + data)
    print(canSend)
    print(CANparse(canSend))