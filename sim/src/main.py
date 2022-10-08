from ast import Pass
import logging
import socket
import time
import math
import struct

#All Data is little endian (smallest index of each field has LSB)
#Should be sent in this format: for i in CAN_Test_Data: return can.CANparse(bytearray(i[3::-1] + i[7:3:-1] + i[16:7:-1]), 1)
CAN_Test_Data = [
#   |         CAN ID       |          IDX          |                     DATA                      |
    [0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01], #Dash Kill Switch On (0)
    [0x00, 0x00, 0x00, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01], #BPS Trip On (1)
    [0x00, 0x00, 0x00, 0x03, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01], #Any System Failure On (2)
    [0x00, 0x00, 0x00, 0x04, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01], #Ignition On (3)
    [0x00, 0x00, 0x00, 0x05, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01], #Any System Shutoff On (4)
    [0x00, 0x00, 0x01, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01], #BPS All Clear Enabled (5)
    [0x00, 0x00, 0x01, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01], #BPS Contactor State On (6)
    [0x00, 0x00, 0x01, 0x03, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x04, 0x0C, 0x03, 0x0F, 0x0F], #BPS Current (7)
    [0x00, 0x00, 0x01, 0x04, 0x00, 0x00, 0x00, 0x05, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0D, 0x71], #BPS Voltage 3441mV (8)
    [0x00, 0x00, 0x01, 0x05, 0x00, 0x00, 0x00, 0x05, 0x00, 0x00, 0x00, 0x06, 0x00, 0x00, 0x94, 0x32], #BPS Temperature 37000ish (9)
    [0x00, 0x00, 0x01, 0x06, 0x00, 0x00, 0x00, 0x00, 0x04, 0x00, 0x00, 0x00, 0x01, 0x01, 0x01, 0x01], #SOC gibberish (10)
    [0x00, 0x00, 0x01, 0x07, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01], #WDOG Triggered True (11)
    [0x00, 0x00, 0x01, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01], #CAN Error True (12)
    #[0x109] - NOT USED
    [0x00, 0x00, 0x01, 0x0B, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0D, 0x75], #Supplemental Voltage 3441mV (13)
    [0x00, 0x00, 0x01, 0x0C, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01], #Charging Enabled (14)

    [0x00, 0x00, 0x05, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01], #Car State On (15)
    [0x00, 0x00, 0x02, 0x42, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0B, 0x00, 0x00, 0x00, 0x0A], #Motor Controller BUS (16)
    [0x00, 0x00, 0x02, 0x43, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x10, 0x00, 0x00, 0x00, 0x00, 0x20], #Velocity (17)
    [0x00, 0x00, 0x02, 0x44, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0D, 0x71, 0x00, 0x00, 0x0D, 0x71], #Motor Controller Phase Current(18)
    [0x00, 0x00, 0x02, 0x45, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0D, 0x71, 0x00, 0x00, 0x0D, 0x71], #Motor Voltage Vector(19)
    [0x00, 0x00, 0x02, 0x46, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0D, 0x71, 0x00, 0x00, 0x0D, 0x71], #Motor Current Vector(20)
    [0x00, 0x00, 0x02, 0x47, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0D, 0x71, 0x00, 0x00, 0x0D, 0x71], #Motor BackEMF(21)
    [0x00, 0x00, 0x02, 0x4B, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0D, 0x71, 0x00, 0x00, 0x0D, 0x71], #Motor Temperature(22)
    [0x00, 0x00, 0x02, 0x4E, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0D, 0x71, 0x00, 0x00, 0x0D, 0x71], #Odometer & Bus Amp Hours(23)
    [0x00, 0x00, 0x02, 0x4F, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01], #Array Contactor Enabled(24)

    [0x00, 0x00, 0x06, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0D, 0x05], #Sunscatter A Array Voltage Setpoint(25)
    [0x00, 0x00, 0x06, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0D, 0x71], #Sunscatter A Array Voltage Measurement(26)
    [0x00, 0x00, 0x06, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0D, 0x71], #Sunscatter A Array Current Measurement(27)
    [0x00, 0x00, 0x06, 0x03, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0D, 0x71], #Sunscatter A Battery Voltage Measurement(28)
    [0x00, 0x00, 0x06, 0x04, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0D, 0x71], #Sunscatter A Battery Current Measurement(29)
    [0x00, 0x00, 0x06, 0x05, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01], #Sunscatter A override enabled(30)
    [0x00, 0x00, 0x06, 0x06, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01], #Sunscatter A Fault Enabled(31)
    [0x00, 0x00, 0x06, 0x10, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0D, 0x71], #Sunscatter B Array Voltage Setpoint(32)
    [0x00, 0x00, 0x06, 0x11, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0D, 0x71], #Sunscatter B Array Voltage Measurement(33)
    [0x00, 0x00, 0x06, 0x12, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0D, 0x71], #Sunscatter B Array Current Measurement(34)
    [0x00, 0x00, 0x06, 0x13, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0D, 0x71], #Sunscatter B Battery Voltage Measurement(35)
    [0x00, 0x00, 0x06, 0x14, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0D, 0x71], #Sunscatter B Battery Current Measurement(36)
    [0x00, 0x00, 0x06, 0x15, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01], #Sunscatter B override enabled(37)
    [0x00, 0x00, 0x06, 0x16, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01] #Sunscatter B fault enabled(38)
]

#                          1         2         3         4         5
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
start_time = time.time()
trip_map = {
    "BPS_Trip": 1,
    "BPS_All_Clear": 1,
    "BPS_Contactor_State": 1,
    "WDG_Trip": 1,
    "Can_Error": 1,
    "Charging_Enabled": 1
}

#this updates the velocity as a sin wave 
def update_GPS_data():
    GPS_Test_Data_array[9] = round(GPS_Test_Data_array[9] + math.sin((time.time() - start_time)/4) * 0.3, 5)
    GPS_Test_Data_array[1] = round(GPS_Test_Data_array[1] + GPS_Test_Data_array[9], 0)
    GPS_Test_Data_array[5] = round(GPS_Test_Data_array[5] + GPS_Test_Data_array[9], 0)
    GPS_Test_Data = ""
    for i in GPS_Test_Data_array:
        GPS_Test_Data += str(i)
        
def triggerBPSTrip():
    trip_map["BPS_Trip"] = 0

def triggerBPSAllClear():
    trip_map["BPS_All_Clear"] = 0

def triggerBPSContactorState():
    trip_map["BPS_Contactor_State"] = 0

def triggerWDGTrip():
    trip_map["WDG_Trip"] = 0

def triggerCanError():
    trip_map["Can_Error"] = 0
    

def add_to_CAN_data(index, data):
    i = CAN_Test_Data[index]
    for k in range(1, len(data)):
        i[len(i) - k] = data[k]
    
def send_data(CAN, index, socket):
    socket.send(bytearray(CAN + index[3::-1] + index[7:3:-1] + index[16:7:-1]))
    
    
def send_bps_contactor_state(CAN, socket):
    if(trip_map["BPS_Contactor_State"] == 0):
        CAN_Test_Data[0][15] = 0x00
    send_data(CAN, CAN_Test_Data[6], socket)
    
def send_WDOG_triggered(CAN, socket):
    if(trip_map["WDG_Trip"] == 0):
        CAN_Test_Data[11][15] = 0x00
    send_data(CAN, CAN_Test_Data[10], socket)
    
def send_CAN_error(CAN, socket):
    if(trip_map["Can_Error"] == 0):
        CAN_Test_Data[12][15] = 0x00
    send_data(CAN, CAN_Test_Data[11], socket)
    
def send_blackbody_board_enable(CAN, socket):
    pass
    
def send_blackbody_board_fault(CAN, socket):
    pass
    
# sends all 1hz data at the CAN index to the socket
def send_1hz_data(CAN, socket):
    send_bps_contactor_state(CAN, socket)
    send_WDOG_triggered(CAN, socket)
    send_CAN_error(CAN, socket)
    send_blackbody_board_enable(CAN, socket)
    send_blackbody_board_fault(CAN, socket)

def send_blackbody_rtd(CAN, socket):
    pass

def send_2hz_data(CAN, socket):
    send_blackbody_rtd(CAN, socket)

def send_bps_trip(CAN, socket):
    if(trip_map["BPS_Trip"] == 0):
        CAN_Test_Data[1][15] = 0x00
    send_data(CAN, CAN_Test_Data[1], socket)
    
def send_current(CAN, socket):
    x = (time.time() - start_time)/60
    y = 3 * math.sin(3*x) + 4.1 * math.cos(x/3+1.2)-6 * math.sin(2.1*x/3-1.6)
    low_bound = -20000
    high_bound = 55000
    y = struct.pack('q', round(low_bound + (high_bound - low_bound) / 26 * (y + 13)))
    add_to_CAN_data(7, y)
    #generates random current data based on a randomly chosen sin wave
    
    send_data(CAN, CAN_Test_Data[7], socket)


    
def send_voltage(CAN, socket):
    x = (time.time() - start_time)/50
    y = 2 * math.cos(x) + 4 * math.cos(3.2 * x)-1.3 * math.sin(x/2.1)
    low_bound = 2500
    high_bound = 4200
    y = struct.pack('q', round(low_bound + (high_bound - low_bound) / 28 * (y + 14)))
    add_to_CAN_data(8, y)
    #update voltage with a randomly chosen sin wave
    
    send_data(CAN, CAN_Test_Data[8], socket)
    
def send_temperature(CAN, socket):
    x = (time.time() - start_time)/60
    y = 23 * math.cos(x/14 + 2)
    low_bound = 0   
    high_bound = 50
    y = struct.pack('i', round(low_bound + (high_bound - low_bound) / 46 * (y + 23)))
    add_to_CAN_data(9, y)
    
    send_data(CAN, CAN_Test_Data[9], socket)
    
def send_state_of_charge(CAN, socket):
    x = (time.time() - start_time)/60
    y = 10 * math.sin(x/10)
    low_bound = 0   
    high_bound = 10000
    y = struct.pack('i', round(low_bound + (high_bound - low_bound) / 20 * (y + 10)))
    add_to_CAN_data(10, y)
    
    send_data(CAN, CAN_Test_Data[10], socket)
    
def send_supplemental_voltage(CAN, socket):
    x = (time.time() - start_time)/60
    y = 17 * math.sin(x/10)
    low_bound = 6000   
    high_bound = 15000
    y = struct.pack('i', round(low_bound + (high_bound - low_bound) / 34 * (y + 17)))
    add_to_CAN_data(13, y)
    
    send_data(CAN, CAN_Test_Data[13], socket)
    
def send_charging_enabled(CAN, socket):
    if(trip_map["Charging_Enabled"] == 0):
        CAN_Test_Data[14][15] = 0x00
    send_data(CAN, CAN_Test_Data[14], socket)

def send_Sunscatter_A_Voltage_Setpoint(CAN, socket):
    x = (time.time() - start_time)/60
    y = 3 * math.sin(3*x) + 4.1 * math.cos(x/3+1.2)-6 * math.sin(2.1*x/3-1.6)
    low_bound = 0
    high_bound = 10
    y = struct.pack('q', round(low_bound + (high_bound - low_bound) / 26 * (y + 13)))
    add_to_CAN_data(25, y)
    #generates random voltage setpoint based on a randomly chosen sin wave
    send_data(CAN, CAN_Test_Data[25], socket)

def send_Sunscatter_B_Voltage_Setpoint(CAN, socket):
    x = (time.time() - start_time)/60
    y = 2 * math.cos(x-3) + 1.2 * math.sin(3*x-1)-1.8* math.sin(x/3+2)
    low_bound = 0
    high_bound = 10
    y = struct.pack('q', round(low_bound + (high_bound - low_bound) / 10 * (y + 5)))
    add_to_CAN_data(32, y)
    #generates random voltage setpoint based on a randomly chosen sin wave
    send_data(CAN, CAN_Test_Data[32], socket)

# sends all 5hz data at the CAN index to the socket
def send_5hz_data(CAN, socket):
    send_bps_trip(CAN, socket)
    send_current(CAN, socket)
    send_voltage(CAN, socket)
    send_temperature(CAN, socket)
    send_state_of_charge(CAN, socket)
    send_supplemental_voltage(CAN, socket)
    send_charging_enabled(CAN, socket)
    send_Sunscatter_A_Voltage_Setpoint(CAN, socket)
    send_Sunscatter_B_Voltage_Setpoint(CAN, socket)

def send_blackbody_irradiance1(CAN, socket):
    pass    

def send_blackbody_irradiance2(CAN, socket):
    pass

def send_10hz_data(CAN, socket):
    send_blackbody_irradiance1(CAN, socket)
    send_blackbody_irradiance2(CAN, socket)


def send_bps_all_clear(CAN, socket):
    if(trip_map["BPS_All_Clear"] == 0):
        CAN_Test_Data[5][15] = 0x00
    send_data(CAN, CAN_Test_Data[5], socket)

def send_Sunscatter_A_Voltage_Measurement(CAN, socket):
    x = (time.time() - start_time)/60
    y = 5 * math.sin(5*x) + 3.5 * math.cos(x/5+1.2)-6 * math.sin(2.1*x/5-1.6)
    low_bound = 0
    high_bound = 10
    y = struct.pack('q', round(low_bound + (high_bound - low_bound) / 30 * (y + 15)))
    add_to_CAN_data(26, y)
    #generates random voltage setpoint based on a randomly chosen sin wave
    send_data(CAN, CAN_Test_Data[26], socket)

def send_Sunscatter_A_Current_Measurement(CAN, socket):
    x = (time.time() - start_time)/60
    y = 3 * math.sin(3*x) + 4.1 * math.cos(x/3+1.2)-6 * math.sin(2.1*x/3-1.6)
    low_bound = 0
    high_bound = 10
    y = struct.pack('q', round(low_bound + (high_bound - low_bound) / 26 * (y + 13)))
    add_to_CAN_data(27, y)
    #generates random voltage setpoint based on a randomly chosen sin wave
    send_data(CAN, CAN_Test_Data[27], socket)

def send_Sunscatter_A_Bat_Voltage_Measurement(CAN, socket):
    x = (time.time() - start_time)/60
    y = 3 * math.sin(3*x) + 4.1 * math.cos(x/3+1.2)-6 * math.sin(2.1*x/3-1.6)
    low_bound = 0
    high_bound = 10
    y = struct.pack('q', round(low_bound + (high_bound - low_bound) / 26 * (y + 13)))
    add_to_CAN_data(28, y)
    #generates random voltage setpoint based on a randomly chosen sin wave
    send_data(CAN, CAN_Test_Data[28], socket)

def send_Sunscatter_A_Bat_Current_Measurement(CAN, socket):
    x = (time.time() - start_time)/60
    y = 3 * math.sin(3*x) + 4.1 * math.cos(x/3+1.2)-6 * math.sin(2.1*x/3-1.6)
    low_bound = 0
    high_bound = 10
    y = struct.pack('q', round(low_bound + (high_bound - low_bound) / 26 * (y + 13)))
    add_to_CAN_data(29, y)
    #generates random voltage setpoint based on a randomly chosen sin wave
    send_data(CAN, CAN_Test_Data[29], socket)
#array B
def send_Sunscatter_B_Voltage_Measurement(CAN, socket):
    x = (time.time() - start_time)/60
    y = 4 * math.sin(3*x + 1) + 5 * math.cos(x/3-1.2)- 9* math.sin(x/9-1.6)
    low_bound = 0
    high_bound = 10
    y = struct.pack('q', round(low_bound + (high_bound - low_bound) / 36 * (y + 18)))
    add_to_CAN_data(33, y)
    #generates random voltage setpoint based on a randomly chosen sin wave
    send_data(CAN, CAN_Test_Data[33], socket)

def send_Sunscatter_B_Current_Measurement(CAN, socket):
    x = (time.time() - start_time)/60
    y = 2 * math.sin(2*x+1) + 5 * math.cos(x/4-1.2)
    low_bound = 0
    high_bound = 10
    y = struct.pack('q', round(low_bound + (high_bound - low_bound) / 14 * (y + 7)))
    add_to_CAN_data(34, y)
    #generates random voltage setpoint based on a randomly chosen sin wave
    send_data(CAN, CAN_Test_Data[34], socket)

def send_Sunscatter_B_Bat_Voltage_Measurement(CAN, socket):
    x = (time.time() - start_time)/60
    y = 7 * math.sin(x/5.3 + 1) + 13 * math.cos(x/3-2)- 17 * math.sin(x/13 + 3)
    low_bound = 0
    high_bound = 10
    y = struct.pack('q', round(low_bound + (high_bound - low_bound) / 74 * (y + 37)))
    add_to_CAN_data(35, y)
    #generates random voltage setpoint based on a randomly chosen sin wave
    send_data(CAN, CAN_Test_Data[35], socket)

def send_Sunscatter_B_Bat_Current_Measurement(CAN, socket):
    x = (time.time() - start_time)/60
    y = 13 * math.cos(x/7 -2)-3 * math.sin(x/13+3)-7 * math.sin(x/5)
    low_bound = 0
    high_bound = 10
    y = struct.pack('q', round(low_bound + (high_bound - low_bound) / 46 * (y + 23)))
    add_to_CAN_data(36, y)
    #generates random voltage setpoint based on a randomly chosen sin wave
    send_data(CAN, CAN_Test_Data[36], socket)

# sends all 50hz data at the CAN index to the socket
def send_50hz_data(CAN, socket):
    send_bps_all_clear(CAN, socket)
    send_Sunscatter_A_Voltage_Measurement
    send_Sunscatter_A_Current_Measurement
    send_Sunscatter_A_Bat_Voltage_Measurement
    send_Sunscatter_A_Bat_Current_Measurement
    send_Sunscatter_B_Voltage_Measurement
    send_Sunscatter_B_Current_Measurement
    send_Sunscatter_B_Bat_Voltage_Measurement
    send_Sunscatter_B_Bat_Current_Measurement

HOST = 'app'
PORT = 65432

#This is the only function that should be called outside of this file. Other functions will be called within this function
def sender():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    logging.debug("Client starting...")
    s.setblocking(True)
    eth_header_CAN = [0x03, 0x10]
    eth_header_GPS = [0x02, len(GPS_Test_Data)]
    eth_header_IMU = [0x01, 0x12]

    hz1 = time.time_ns()
    hz2 = time.time_ns()
    hz5 = time.time_ns()
    hz10 = time.time_ns()
    hz50 = time.time_ns()
    nanosecond = 1000000000
    
    #update time update for GPS update
    hzGPS = time.time_ns()
    hzIMU = time.time_ns()

    while True:
        cur_time = time.time_ns()
        
        if((cur_time - hz1) > nanosecond):
            hz1 = cur_time
            send_1hz_data(eth_header_CAN, s)
            logging.debug("CAN sent at 1hz.")
            
        if((cur_time - hz2) > nanosecond/2):
            hz2 = cur_time
            send_2hz_data(eth_header_CAN, s)
            logging.debug("CAN sent at 2hz.")
            
        if(cur_time - hz5 > nanosecond/5):
            hz5 = cur_time
            send_5hz_data(eth_header_CAN, s)
            logging.debug("CAN sent at 5hz.")
            
        if(cur_time - hz10 > nanosecond/10):
            hz10 = cur_time
            send_10hz_data(eth_header_CAN, s)
            logging.debug("CAN sent at 10hz.")
            
        if(cur_time - hz50 > nanosecond/50):
            hz50 = cur_time
            send_50hz_data(eth_header_CAN, s)
            logging.debug("CAN sent at 50hz.")
            

        # for i in CAN_Test_Data: 
        # s.send(bytearray(eth_header_CAN + i[3::-1] + i[7:3:-1] + i[16:7:-1]) )
        
        #temporary place holder, unknown how much polling is gps
        if(cur_time - hzGPS > nanosecond/2):
            hzGPS = cur_time
            update_GPS_data()
            s.sendall(bytearray(eth_header_GPS) + GPS_Test_Data.encode())
            logging.debug("GPS sent.")
            
        #temporary place holder, unknown how much polling is imu
        if(cur_time - hzIMU > nanosecond/2):
            hzIMU = cur_time
            for i in IMU_Test_Data:
                s.sendall(bytearray(eth_header_IMU) + i)
            logging.debug("IMU sent.")

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    # HOST = 'localhost'
    # PORT = 65432
    sender()
