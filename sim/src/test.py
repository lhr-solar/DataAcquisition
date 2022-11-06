import struct
import random
import time
import numpy as np

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
       
GPS_Test_Data = "064951000A3855.5137N09540.4829W30.4141.482604063.05W"
# 38.9252284 -95.6747154 topeka coords
 
def generateGPS(lat, lon, speed) -> bytearray:
    gps = "064951000A" + f'{abs(int(lat)):02}' + f'{(abs(lat)%1)*60:02.4f}' + ("N" if lat > 0 else "S") + f'{abs(int(lon)):03}' + f'{(abs(lon)%1)*60:02.4f}' + ("E" if lon > 0 else "W") + f'{speed/1.15078:02.4f}' + ".482604063.05W"
    print(gps)
    print(GPS_Test_Data)
    return bytearray(0x10) + gps.encode()

generateGPS(38.9252284, -95.6747154, 40)

# while True:
#     time.sleep(1)
