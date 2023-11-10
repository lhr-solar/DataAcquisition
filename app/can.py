import struct
import logging
from influxdb_client import Point

# what to do with "reserved"

def float_func(load):
    return struct.unpack('<If', load[0:8]) + (0,)

def fixed_func(load):
    unpacked = struct.unpack('<Iq', load[0:12])
    unpacked_list = list(unpacked)
    unpacked_list[1] /= 1000000
    return tuple(unpacked_list) + (0,) # 0s are used for padding

def unsigned_func(load):
    return struct.unpack('<IQ', load[0:12]) + (0,)

def signed_func(load):
    return struct.unpack('<Ii', load[0:8]) + (0,)

def two_word_func(load):
    return struct.unpack('<III', load[0:12])

def index_func(load):
    return struct.unpack('<II', load[0:8]) + (0,) # ^^ issue b/c some data fields may not be unsigned int?

# returns bit value from bytearray given the index of the bit in byte array
def access_bit(data, index):
    base = int(index // 8)
    shift = int(index % 8)
    return (data[base] >> shift) & 0x1


def byteArrayToList(bytearr):
    bitarr = []
    for byte in bytearr:
        for i in range(7, -1, -1):  # Iterate through each bit in the byte
            bit = (byte >> i) & 1  # Extract the i-th bit
            bitarr.append(bit)
    return bitarr



def bits_to_uint16(bit_list):
    binary_str = ''.join(map(str, bit_list))
    # Convert the binary string to a uint16 integer
    uint16_int = int(binary_str, 2)
    return uint16_int


def parseMotorStatus(load):
    print("start parsing motor status")
    returnList = (0) * 29 # 29 is the number of fields we need for motor status

    # load is the index + data
    # [4:] will grab the data and ignore the index
    byteList = byteArrayToList(load[4:])

    # We are setting the bits from the data and putting it into the list, with each element in the list being a field for the tuple
    # set the individual bits from [0-6] equal to that of the data
    for i in range(7):
        returnList[i] = byteList[i]

    # 7-15 are reserved so we will keep them at 0

    # set individual bits from 16-24
    for i in range(16, 25):
        returnList[i] = byteList[i]

    # 25-31 are reserved so we will keep them at 0

    # compute the value for bits 16-31 for the next field
    

    # compute value for bits 32-47 for active motor index

    # compute value for bits 48-55 for transmit error count

    # compute value for bits 56-63 for recieve error count

    return tuple(returnList)


# for the CAN messages that require their own parsing we are creating a function above and placing that as the function to call
# when we need to parse that CAN message's data
CANIDs = {
    0x001: ["Dash Kill Switch",                                 unsigned_func], # correct
    0x002: ["BPS Trip",                                         unsigned_func], # correct
    0x003: ["Any System Failures",                              unsigned_func], # correct
    0x004: ["Ignition",                                         unsigned_func], # correct
    0x005: ["Any System Shutoff",                               unsigned_func], # correct

    0x101: ["BPS All Clear",                                    unsigned_func], # correct
    0x102: ["BPS Contactor State",                              unsigned_func], # correct
    0x103: ["Current Data",                                     signed_func],  # correct      #used to be unsigned
    0x104: ["Voltage Data Array",                               index_func], # correct
    0x105: ["Temperature Data Array",                           index_func], # correct
    0x106: ["State of Charge Data",                             fixed_func],  # correct       #used to be unsigned 
    0x107: ["WDog Triggered",                                   unsigned_func], # correct
    0x108: ["CAN Error",                                        unsigned_func], # correct
    0x109: ["BPS Command msg",                                  unsigned_func],             # ^^ doesn't mention type of data
    0x10B: ["Supplemental Voltage",                             unsigned_func], # correct
    0x10C: ["Charging Enabled",                                 unsigned_func], # correct

    # 0x580: ["Car State",                                        unsigned_func],     #not used 
    0x580: ["CONTROL_MODE",                                     signed_func], # ^^ unsure of function
    # 0x581: ["Car Data",                                         unsigned_func], #^^ should be IO_STATE # unsure of type -> function
    0x581: ["IO_STATE", "Contactor Bitmap", "Switch Bitmap", "Brake Pedal", "Accel Pedal", two_word_func], # ^^ updated
    0x240: ["Motor Controller Identification", "Device serial number", "Prohelion ID",  two_word_func],  #^^ added
    
    # ^^ what to do with reserved, was this done correctly?
    0x241: ["Motor Status", "Receive error count", "Transmit error count", "Active Motor index", "Error Flags", 
            "Reserved", "Motor Over Speed", "Desaturation fault", "15V rail under voltage lock out", "Config read error",
            "Watchdog caused last reset", "Bad motor position hall sequence", "DC Bus over voltage", "Software over current",
            "Hardware over current", "Limit Flags", "Reserved", "IPM or Motor Temperature", "Bus Voltage Lower Limit", 
            "Bus Voltage Upper Limit", "Bus Current", "Velocity", "Motor Current", "Output Voltage PWM", parseMotorStatus],
    
    0x242: ["Motor Controller Bus", "Current", "Voltage",       two_word_func], # correct
    0x243: ["Velocity", "m/s", "rpm",                           two_word_func], # correct
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

    0x620: ["Blackbody RTD Sensor Measurement",                 index_func],
    #0x621: ["Set Mode", ""]
    0x622: ["Blackbody (Irradiance/RTD) Board Fault", "Error ID",                                       unsigned_func], # New Line, Blackbody Irradiance had wrong can id
    0x623: ["Acknowledge Fault", "x01 - Acknowledge Fault, return to STOP state",                       two_word_func], # New Line
    0x624: ["RTD Configure", "Enabled RTDs", "RTD Sample Frequency (Hz)",                               two_word_func], # New Line
    0x625: ["Irradiance Configure", "Enabled Irradiance Sensor", "Irradiance Sample Frequency (Hz)",    two_word_func], # New Line
    0x626: ["Blackbody (RTD Sensor) Measurement", "RTD ID" "Temperature Measurment",                    two_word_func], # New line, name & can id was wrong
    0x627: ["Blackbody Irradiance Measurement", "Irradiance Sensor ID", "Irradiance Measuement",        two_word_func], # New Line 
    #0x630: ["Blackbody Irradiance Sensor 1 Measurement",        float_func], # Wrong Can ID
    #0x631: ["Blackbody Irradiance Sensor 2 Measurement",        float_func], # Wrong can ID
    #0x632: ["Blackbody Irradiance Board command",               unsigned_func], # Not Used
    #0x633: ["Blackbody Irradiance Board Fault",                 unsigned_func],
    0x640: ["PV Curve Tracer Profile", "Test ID", "Test Regime", "Start PWM", "PWMResolution",          unsigned_func] # Updated Fields, Now Correct
}


def CANparse(data):

    print("Data in CANparse: ", data) # ^ I added for test
    logging.debug(data)
    print("CAN ID Bytes: ", data[0:4])
    canID = int.from_bytes(data[0:4], "little")
    
    print("Can ID ID: ", canID)
    logging.debug(canID)
    # print("special can ID dict keys", specialCanIds)
    # check for special can IDs we need to parse seperate from rest
    
    packet = CANIDs[canID][-1](data[4:])
    # print("packet: ", packet) 
    # print()

    if (packet[2] == 0): 
        logging.debug(CANIDs[canID][0] + ": " + str(packet[1]) + "\n")
    else:
        logging.debug(CANIDs[canID][0] + "->" + CANIDs[canID][1] + ": " + str(packet[1]))
        logging.debug(CANIDs[canID][0] + "->" + CANIDs[canID][2] + ": " + str(packet[2]) + "\n")

    return (Point(CANIDs[canID][0]).field(packet[0], packet[1]) #return just index and data
        if (packet[2] == 0) # check for 0 padding b/c then will be: unsigned, signed, index functions
        else 
            [Point(CANIDs[canID][0]).field(CANIDs[canID][i], packet[i]) #return data type and data for both data fields
            for i in [1,2]] 
    )


if __name__ == "__main__":

    # need to flip the can id, the index, and the data individually
    # and then pass it into the CAnparse function

    
    motor_status = bytearray([0x00, 0x00, 0x02, 0x41, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x01, 0x00, 0x00, 0x00])
    CANparse(motor_status)

    # print()
    # print()
    # testing to see how we need to access values

    # WDOG_Triggered = [0x00, 0x00, 0x06, 0x24, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01] #WDOG Triggered True
    # CANparse(WDOG_Triggered) #unsigned_func(WDOG_Triggered)

