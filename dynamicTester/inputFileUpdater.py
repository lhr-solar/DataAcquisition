import struct


i = 103
y = hex(i)
print(y)
print(hex(int(y[2:4], 16)))
print(len(y))

var = struct.pack('<III', 0, 3, 15)
print(var)
print(struct.unpack('<III', var))
#print(struct.unpack('<III', b'\xf8\xfe\x01\x00\xbe\x03\x82\xfc\xaa\xfe\xcc\xfc\x00\x00\xfe\xff\x02\x00'))
print(struct.unpack('<III', b'\x00\x00\x00\x00\x00\x00\x0D\x71\x00\x00\x0D\x71'))

data = -15000
data = struct.pack('q',data)
print(data)
print(len(data))
print(hex(data[8]))