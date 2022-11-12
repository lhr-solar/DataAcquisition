#Sunlight as socket CLIENT
import logging
import socket
import time
import struct
import random

#All Data is little endian (smallest index of each field has LSB)
#Should be sent in this format: for i in CAN_Test_Data: return can.CANparse(bytearray(i[3::-1] + i[7:3:-1] + i[16:7:-1]), 1)
CAN_Test_Data = [
#   |         CAN ID       |          IDX          |                     DATA                      |
    [0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01], #Dash Kill Switch On
    [0x00, 0x00, 0x00, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01], #BPS Trip On
    [0x00, 0x00, 0x00, 0x03, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01], #Any System Failure On
    [0x00, 0x00, 0x00, 0x04, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01], #Ignition On
    [0x00, 0x00, 0x00, 0x05, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01], #Any System Shutoff On
    [0x00, 0x00, 0x01, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01], #BPS All Clear Enabled
    [0x00, 0x00, 0x01, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01], #BPS Contactor State On
    [0x00, 0x00, 0x01, 0x03, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x3A, 0x98], #BPS Current 3A
    [0x00, 0x00, 0x01, 0x04, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0D, 0x71], #BPS Voltage 3441mV
    [0x00, 0x00, 0x01, 0x04, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0D, 0x71], #BPS Voltage 3441mV
    [0x00, 0x00, 0x01, 0x04, 0x00, 0x00, 0x00, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0D, 0x71], #BPS Voltage 3441mV
    [0x00, 0x00, 0x01, 0x04, 0x00, 0x00, 0x00, 0x03, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0D, 0x71], #BPS Voltage 3441mV
    [0x00, 0x00, 0x01, 0x04, 0x00, 0x00, 0x00, 0x04, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0D, 0x71], #BPS Voltage 3441mV
    [0x00, 0x00, 0x01, 0x04, 0x00, 0x00, 0x00, 0x05, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0D, 0x71], #BPS Voltage 3441mV
    [0x00, 0x00, 0x01, 0x04, 0x00, 0x00, 0x00, 0x06, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0D, 0x71], #BPS Voltage 3441mV
    [0x00, 0x00, 0x01, 0x04, 0x00, 0x00, 0x00, 0x07, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0D, 0x71], #BPS Voltage 3441mV
    [0x00, 0x00, 0x01, 0x04, 0x00, 0x00, 0x00, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0D, 0x71], #BPS Voltage 3441mV
    [0x00, 0x00, 0x01, 0x04, 0x00, 0x00, 0x00, 0x09, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0D, 0x71], #BPS Voltage 3441mV
    [0x00, 0x00, 0x01, 0x04, 0x00, 0x00, 0x00, 0x0A, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0D, 0x71], #BPS Voltage 3441mV
    [0x00, 0x00, 0x01, 0x04, 0x00, 0x00, 0x00, 0x0B, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0D, 0x71], #BPS Voltage 3441mV
    [0x00, 0x00, 0x01, 0x04, 0x00, 0x00, 0x00, 0x0C, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0D, 0x71], #BPS Voltage 3441mV
    [0x00, 0x00, 0x01, 0x04, 0x00, 0x00, 0x00, 0x0D, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0D, 0x71], #BPS Voltage 3441mV
    [0x00, 0x00, 0x01, 0x04, 0x00, 0x00, 0x00, 0x0E, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0D, 0x71], #BPS Voltage 3441mV
    [0x00, 0x00, 0x01, 0x04, 0x00, 0x00, 0x00, 0x0F, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0D, 0x71], #BPS Voltage 3441mV
    [0x00, 0x00, 0x01, 0x04, 0x00, 0x00, 0x00, 0x10, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0D, 0x71], #BPS Voltage 3441mV
    [0x00, 0x00, 0x01, 0x04, 0x00, 0x00, 0x00, 0x11, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0D, 0x71], #BPS Voltage 3441mV
    [0x00, 0x00, 0x01, 0x04, 0x00, 0x00, 0x00, 0x12, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0D, 0x71], #BPS Voltage 3441mV
    [0x00, 0x00, 0x01, 0x04, 0x00, 0x00, 0x00, 0x13, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0D, 0x71], #BPS Voltage 3441mV
    [0x00, 0x00, 0x01, 0x04, 0x00, 0x00, 0x00, 0x14, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0D, 0x71], #BPS Voltage 3441mV
    [0x00, 0x00, 0x01, 0x04, 0x00, 0x00, 0x00, 0x15, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0D, 0x71], #BPS Voltage 3441mV
    [0x00, 0x00, 0x01, 0x04, 0x00, 0x00, 0x00, 0x16, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0D, 0x71], #BPS Voltage 3441mV
    [0x00, 0x00, 0x01, 0x04, 0x00, 0x00, 0x00, 0x17, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0D, 0x71], #BPS Voltage 3441mV
    [0x00, 0x00, 0x01, 0x04, 0x00, 0x00, 0x00, 0x18, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0D, 0x71], #BPS Voltage 3441mV
    [0x00, 0x00, 0x01, 0x04, 0x00, 0x00, 0x00, 0x19, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0D, 0x71], #BPS Voltage 3441mV
    [0x00, 0x00, 0x01, 0x04, 0x00, 0x00, 0x00, 0x1A, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0D, 0x71], #BPS Voltage 3441mV
    [0x00, 0x00, 0x01, 0x04, 0x00, 0x00, 0x00, 0x1B, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0D, 0x71], #BPS Voltage 3441mV
    [0x00, 0x00, 0x01, 0x04, 0x00, 0x00, 0x00, 0x1C, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0D, 0x71], #BPS Voltage 3441mV
    [0x00, 0x00, 0x01, 0x04, 0x00, 0x00, 0x00, 0x1D, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0D, 0x71], #BPS Voltage 3441mV
    [0x00, 0x00, 0x01, 0x04, 0x00, 0x00, 0x00, 0x1E, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0D, 0x71], #BPS Voltage 3441mV
    [0x00, 0x00, 0x01, 0x04, 0x00, 0x00, 0x00, 0x1F, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0D, 0x71], #BPS Voltage 3441mV
    [0x00, 0x00, 0x01, 0x05, 0x00, 0x00, 0x00, 0x05, 0x00, 0x00, 0x00, 0x06, 0x00, 0x00, 0x00, 0x55], #BPS Temperature 85
    [0x00, 0x00, 0x01, 0x06, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x05, 0x5D, 0x4A, 0x80], #SOC 90%
    [0x00, 0x00, 0x01, 0x07, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01], #WDOG Triggered True
    [0x00, 0x00, 0x01, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01], #CAN Error True
    #[0x109] - NOT USED
    [0x00, 0x00, 0x01, 0x0B, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x27, 0x0F], #Supplemental Voltage 9999mV
    [0x00, 0x00, 0x01, 0x0C, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01], #Charging Enabled

    [0x00, 0x00, 0x05, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01], #Car State On
    [0x00, 0x00, 0x02, 0x42, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x64, 0x00, 0x00, 0x00, 0x0C], #Motor Controller Bus 12V 100A
    [0x00, 0x00, 0x02, 0x43, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x03, 0xE8, 0x00, 0x00, 0x00, 0x05], #Velocity 5m/s 1000rpm
    [0x00, 0x00, 0x02, 0x44, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xF0, 0x00, 0x00, 0x00, 0xFA], #Motor Controller Phase Current 250+j240
    [0x00, 0x00, 0x02, 0x45, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0A, 0x00, 0x00, 0x00, 0x0C], #Motor Voltage Vector 12+j10
    [0x00, 0x00, 0x02, 0x46, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x08, 0x00, 0x00, 0x00, 0x03], #Motor Current Vector 3+j8
    [0x00, 0x00, 0x02, 0x47, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x03, 0x00, 0x00, 0x00, 0x02], #Motor BackEMF 2V 3V
    [0x00, 0x00, 0x02, 0x4B, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x64, 0x00, 0x00, 0x00, 0x5F], #Motor Temperature 95 100
    [0x00, 0x00, 0x02, 0x4E, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02, 0x00, 0x00, 0x00, 0x0A], #Odometer/Bus Amp Hours 10 2
    [0x00, 0x00, 0x02, 0x4F, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01], #Array Contactor Enabled

    [0x00, 0x00, 0x06, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x41, 0x40, 0x00, 0x00], #Sunscatter A Array Voltage Setpoint 12V
    [0x00, 0x00, 0x06, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x41, 0x40, 0x00, 0x00], #Sunscatter A Array Voltage Measurement 12V
    [0x00, 0x00, 0x06, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x41, 0x70, 0x00, 0x00], #Sunscatter A Array Current Measurement 15A
    [0x00, 0x00, 0x06, 0x03, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x41, 0x30, 0x00, 0x00], #Sunscatter A Battery Voltage Measurement 11V
    [0x00, 0x00, 0x06, 0x04, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x41, 0x60, 0x00, 0x00], #Sunscatter A Battery Current Measurement 14A
    [0x00, 0x00, 0x06, 0x05, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01], #Sunscatter A Override Enabled
    [0x00, 0x00, 0x06, 0x06, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01], #Sunscatter A Fault Enabled
    [0x00, 0x00, 0x06, 0x10, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x41, 0x10, 0x00, 0x00], #Sunscatter B Array Voltage Setpoint 9V
    [0x00, 0x00, 0x06, 0x11, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x41, 0x20, 0x00, 0x00], #Sunscatter B Array Voltage Measurement 10V
    [0x00, 0x00, 0x06, 0x12, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x41, 0x50, 0x00, 0x00], #Sunscatter B Array Current Measurement 13A
    [0x00, 0x00, 0x06, 0x13, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x41, 0x10, 0x00, 0x00], #Sunscatter B Battery Voltage Measurement 9V
    [0x00, 0x00, 0x06, 0x14, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x41, 0x40, 0x00, 0x00], #Sunscatter B Battery Current Measurement 12A
    [0x00, 0x00, 0x06, 0x15, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01], #Sunscatter B Override Enabled
    [0x00, 0x00, 0x06, 0x16, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01], #Sunscatter B Fault Enabled
]

#                          1         2         3         4         5
#                0123456789012345678901234567890123456789012345678901
GPS_Test_Data = "064951000A3855.5137N09540.4829W30.4141.482604063.05W"
# 38.9252284 -95.6747154 topeka coords

IMU_Test_Data = [                                                                           # Accelerometer:Magnetometer:Gyroscope           
    bytearray(b'\xf8\xfe\x01\x00\xbe\x03\x82\xfc\xaa\xfe\xcc\xfc\x00\x00\xfe\xff\x02\x00'), #-264, 1, 958:-894, -342, -820:  0, -2,  2
    bytearray(b'\xf9\xfe\x00\x00\xbb\x03\x82\xfc\xaa\xfe\xcc\xfc\xfb\xff\xff\xff\x06\x00'), #-263, 0, 995:-894, -342, -820:  0, -2,  2
    bytearray(b'\xfa\xfe\x01\x00\xbe\x03\x82\xfc\xaa\xfe\xcc\xfc\xf3\xff\xfa\xff\x0b\x00'), #-262, 1, 958:-894, -342, -820:-13, -6, 11
]   

HOST = 'app'
PORT = 65432
eth_header_CAN = [0x03, 0x10]
eth_header_GPS = [0x02, 0x34]
eth_header_IMU = [0x01, 0x12]

def generateGPS(lat, lon, speed) -> bytearray:
    gps = "064951000A" + f'{int(abs(lat)):02}' + f'{(abs(lat)%1)*60:02.4f}' + ("N" if lat > 0 else "S") + f'{int(abs(lon)):03}' + f'{(abs(lon)%1)*60:02.4f}' + ("E" if lon > 0 else "W") + f'{speed/1.15078:02.4f}' + ".482604063.05W"
    return bytearray(eth_header_GPS) + gps.encode()

def generateIMU(lower, upper) -> bytearray:
    buf = bytearray(20)
    struct.pack_into('bb', buf, 0, eth_header_IMU[0], eth_header_IMU[1])
    for i in range(1, 10):
        struct.pack_into('h', buf, i*2, random.randrange(lower, upper))
    return buf

def move(start, target):
    if move.count == 30:
        move.lat, move.lon = start
    if move.count > 0:
        move.lat += (abs(target[0]-start[0]))/30 * (-1 if target[0] < start[0] else 1)
        move.lon += (abs(target[1]-start[1]))/30 * (-1 if target[1] < start[1] else 1)
        move.count -= 1
        return generateGPS(move.lat, move.lon, 40)
move.count = 30
move.lat = 0
move.lon = 0

def reconnect_socket(client: socket) -> socket:

    logging.warning("Client disconnect")
    client.close()
    logging.debug("Client reconnecting...")
    return socket.create_connection(address=(HOST, PORT))

class ServerDisconnectError(Exception): pass

#This is the only function that should be called outside of this file. Other functions will be called within this function
def sender():
    s = socket.create_connection(address=(HOST, PORT))
    logging.debug("Client starting...")
    s.setblocking(True)
    while True:
        try:
            for i in CAN_Test_Data: 
                s.send(bytearray(eth_header_CAN + i[3::-1] + i[7:3:-1] + i[16:7:-1]))
            logging.debug("CAN sent.")
            s.sendall(move((38.92959, -95.677242), (38.926558, -95.676713)))
            logging.debug("GPS sent.")
            s.sendall(generateIMU(-1000, 1000))
            logging.debug("IMU sent.")
            time.sleep(1)
            
        except:
            s = reconnect_socket(s)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    sender()