import logging
import socket
import time
import struct
import random

# this is weird and irrelevent for now

# eth_header_IMU = [0x01, 0x12]
# count = 1

# def generateIMU(lower, upper):
#     buf = []
#     for i in range(9):
#         buf [i] = random.randrange(lower, upper)
#     return buf

# def smooth(delay):
#     if smooth.count == 1:
#         smooth.target = generateIMU(-1000, 1000)
#     elif smooth.count == delay:
#         smooth.count = 0
#         smooth.current = smooth.target
#     else:
#         smooth.count += 1
        
        
#     print(bytearray(eth_header_IMU + smooth.current))
    
#     print(smooth.current)

# smooth.count = 1
# smooth.current = generateIMU(-1000, 1000)

eth_header_CAN = [0x03, 0x10]
eth_header_GPS = [0x02, 0x34]
eth_header_IMU = [0x01, 0x12]       


GPS_Test_Data = "064951000A3855.5137N09540.4829W30.4141.482604063.05W"
# 38.9252284 -95.6747154 topeka coords
 
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

for i in range(30):
    print(move((38.931040,-95.677832), (38.919812,-95.675766)))