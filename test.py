import struct

var = struct.pack('<III', 0, , 15)
print(var)
print(struct.unpack('<III', var))
print(struct.unpack('<III', b'\x00\x00\x00\x00\x00\x00\x0D\x71\x00\x00\x0D\x71'))
