import can
import gps
import imu

CAN_Test_Data = [
    0x0010100, #Dash Kill Switch off
    0x0020101, #BPS Trip On
    0x0030101, #Any System Failure On
    0x0040101, #Ignition On
    0x0050101, #Any System Shutoff On
    0x1010101, #BPS All Clear Enabled
    0x1020101, #BPS Contactor State On
    0x10304FCF3FFFF, #BPS Current
    0x1040500000D7100, #BPS Voltage 3441mV
    0x105050600009432, #BPS Temperature 37000ish
    0x1060401010101, #SOC gibberish
    0x1070101, #WDOG Triggered True
    0x1080101, #CAN Error True
    #0x109 - NOT USED
    0x10B020D71, #Supplemental Voltage 3441mV
    0x10C0101, #Charging Enabled

    0x5800101, #Car State On
    0x2420800000D7100000D71, #Gibberish for these too
    0x2430800000D7100000D71,
    0x2440800000D7100000D71,
    0x2450800000D7100000D71,
    0x2460800000D7100000D71,
    0x2470800000D7100000D71,
    0x24B0800000D7100000D71,
    0x24E0800000D7100000D71,
    0x24F0101, #Array Contactor Enabled

    0x6000400000D71, #More Gibberish
    0x6010400000D71,
    0x6020400000D71,
    0x6030400000D71,
    0x6040400000D71,
    0x6050101, #Sunscatter A override enabled
    0x6060101, #Sunscatter A Fault Enabled
    0x6100400000D71, #some hoogaboogah
    0x6110400000D71,
    0x6120400000D71,
    0x6130400000D71,
    0x6140400000D71,
    0x6150101, #Sunscatter B override enabled
    0x6160101, #Sunscatter B fault enabled
]

def can_test():
    for i in CAN_Test_Data: can.CANparse(CAN_Test_Data[i])

if __name__ == "__main__":
    can_test()