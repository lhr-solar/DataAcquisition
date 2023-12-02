from influxdb_client import Point
from can import CANparse


# Testing Function
def specific_can_msg(test_list, correct_list):
    # Convert to Function's Prefered format
    canID = test_list[3::-1]
    idx = test_list[7:3:-1]
    data = test_list[16:7:-1]
    test_byteArray = bytearray(canID + idx + data)

    # Call the Function
    points_list = CANparse(test_byteArray)

    ############## Run the Tests ##############
    
    assert len(correct_list) == len(points_list)                                # Assert Num Points

    for i in range(len(points_list)):                     # Loop Through All Elements in Point List
        point = points_list[i]

        assert isinstance(point, Point)                                         # Assert Point
        #assert point.measurement == "IO_STATE"                                 # Assert Measrument
        assert point._fields == {correct_list[i][0]: correct_list[i][1]}        # Assert Field
        assert point._tags == {}                                                # Assert Tag




def test_CANparse_Motor_Status():

    # Init Test Case 1 - All 0
    #            |         CAN ID       |          IDX          |                     DATA                      |
    test_list1 = [0x00, 0x00, 0x02, 0x41, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
    #                                                          |63-56|55-48|47-40|39-32|31-24|23-16|15-08|07-00|
    correct_list1 = [('Output Voltage PWM',                 1),
                    ('Motor Current',                       1),
                    ('Velocity',                            1),
                    ('Bus Current',                         1),
                    ('Bus Voltage Upper Limit',             1),
                    ('Bus Voltage Lower Limit',             1),
                    ('IPM or Motor Temperature',            1),
                    ('Hardware over current',               1),
                    ('Software over current',               1),
                    ('DC Bus over voltage',                 1),
                    ('Bad motor position hall sequence',    1),
                    ('Watchdog caused last reset',          1),
                    ('Config read error',                   1),
                    ('15V rail under voltage lock out',     1),
                    ('Desaturation fault',                  1),
                    ('Motor Over Speed',                    1),
                    ('Active Motor index',              65535),
                    ('Transmit error count',              255),
                    ('Receive error count',               255)]


    # Init Test Case 2 - All 1
    #            |         CAN ID       |          IDX          |                     DATA                      |
    test_list2 = [0x00, 0x00, 0x02, 0x41, 0xFF, 0xFF, 0xFF, 0xFF, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
    #                                                          |63-56|55-48|47-40|39-32|31-24|23-16|15-08|07-00|
    correct_list2 = [('Output Voltage PWM',                 0),
                    ('Motor Current',                       0),
                    ('Velocity',                            0),
                    ('Bus Current',                         0),
                    ('Bus Voltage Upper Limit',             0),
                    ('Bus Voltage Lower Limit',             0),
                    ('IPM or Motor Temperature',            0),
                    ('Hardware over current',               0),
                    ('Software over current',               0),
                    ('DC Bus over voltage',                 0),
                    ('Bad motor position hall sequence',    0),
                    ('Watchdog caused last reset',          0),
                    ('Config read error',                   0),
                    ('15V rail under voltage lock out',     0),
                    ('Desaturation fault',                  0),
                    ('Motor Over Speed',                    0),
                    ('Active Motor index',                  0),
                    ('Transmit error count',                0),
                    ('Receive error count',                 0)]


    # Init Test Case 3 - Alternate 1010... 
    #            |         CAN ID       |          IDX          |                     DATA                      |
    test_list3 =  [0x00, 0x00, 0x02, 0x41, 0xFF, 0xFF, 0xFF, 0xFF, 0x55, 0x55, 0x55, 0x55, 0x55, 0x55, 0x55, 0x55] # 1010...
    #                                                           |63-56|55-48|47-40|39-32|31-24|23-16|15-08|07-00|
    correct_list3 = [('Output Voltage PWM',                 1),
                    ('Motor Current',                       0),
                    ('Velocity',                            1),
                    ('Bus Current',                         0),
                    ('Bus Voltage Upper Limit',             1),
                    ('Bus Voltage Lower Limit',             0),
                    ('IPM or Motor Temperature',            1),
                    ('Hardware over current',               1), # 1 b/c some reserved inbetween this and the last one
                    ('Software over current',               0),
                    ('DC Bus over voltage',                 1),
                    ('Bad motor position hall sequence',    0),
                    ('Watchdog caused last reset',          1),
                    ('Config read error',                   0),
                    ('15V rail under voltage lock out',     1),
                    ('Desaturation fault',                  0),
                    ('Motor Over Speed',                    1),
                    ('Active Motor index',                  21845),
                    ('Transmit error count',                85),
                    ('Receive error count',                 85)]




    # Init Test Case 4 - Alternate 0101... 
    #            |         CAN ID       |          IDX          |                     DATA                      |
    test_list4 = [0x00, 0x00, 0x02, 0x41, 0xFF, 0xFF, 0xFF, 0xFF, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA] # 0101...
    #                                                           |63-56|55-48|47-40|39-32|31-24|23-16|15-08|07-00|
    correct_list4 = [('Output Voltage PWM',                 0),
                    ('Motor Current',                       1),
                    ('Velocity',                            0),
                    ('Bus Current',                         1),
                    ('Bus Voltage Upper Limit',             0),
                    ('Bus Voltage Lower Limit',             1),
                    ('IPM or Motor Temperature',            0),
                    ('Hardware over current',               0), # 1 b/c some reserved inbetween this and the last one
                    ('Software over current',               1),
                    ('DC Bus over voltage',                 0),
                    ('Bad motor position hall sequence',    1),
                    ('Watchdog caused last reset',          0),
                    ('Config read error',                   1),
                    ('15V rail under voltage lock out',     0),
                    ('Desaturation fault',                  1),
                    ('Motor Over Speed',                    0),
                    ('Active Motor index',                  43690),
                    ('Transmit error count',                170),
                    ('Receive error count',                 170)]


    # Init Test Case 5 - Alternate 00110011001100110011... 
    #            |         CAN ID       |          IDX          |                     DATA                      |
    test_list5 =  [0x00, 0x00, 0x02, 0x41, 0xFF, 0xFF, 0xFF, 0xFF, 0xCC, 0xCC, 0xCC, 0xCC, 0xCC, 0xCC, 0xCC, 0xCC] # 0011..
    #                                                           |63-56|55-48|47-40|39-32|31-24|23-16|15-08|07-00|
    correct_list5 = [('Output Voltage PWM',                 0),
                    ('Motor Current',                       0),
                    ('Velocity',                            1),
                    ('Bus Current',                         1),
                    ('Bus Voltage Upper Limit',             0),
                    ('Bus Voltage Lower Limit',             0),
                    ('IPM or Motor Temperature',            1),
                    ('Hardware over current',               0), # note: some reserved inbetween this and the last one
                    ('Software over current',               0),
                    ('DC Bus over voltage',                 1),
                    ('Bad motor position hall sequence',    1),
                    ('Watchdog caused last reset',          0),
                    ('Config read error',                   0),
                    ('15V rail under voltage lock out',     1),
                    ('Desaturation fault',                  1),
                    ('Motor Over Speed',                    0),
                    ('Active Motor index',                  52428),
                    ('Transmit error count',                204),
                    ('Receive error count',                 204)]



    # Init Test Case 6 - Alternate 11001100110011001100... 
    #            |         CAN ID       |          IDX          |                     DATA                      |
    test_list6 =  [0x00, 0x00, 0x02, 0x41, 0xFF, 0xFF, 0xFF, 0xFF, 0x33, 0x33, 0x33, 0x33, 0x33, 0x33, 0x33, 0x33] 
    #                                                           |63-56|55-48|47-40|39-32|31-24|23-16|15-08|07-00|
    correct_list6 = [('Output Voltage PWM',                 1),
                    ('Motor Current',                       1),
                    ('Velocity',                            0),
                    ('Bus Current',                         0),
                    ('Bus Voltage Upper Limit',             1),
                    ('Bus Voltage Lower Limit',             1),
                    ('IPM or Motor Temperature',            0),
                    ('Hardware over current',               1), # note: some reserved inbetween this and the last one
                    ('Software over current',               1),
                    ('DC Bus over voltage',                 0),
                    ('Bad motor position hall sequence',    0),
                    ('Watchdog caused last reset',          1),
                    ('Config read error',                   1),
                    ('15V rail under voltage lock out',     0),
                    ('Desaturation fault',                  0),
                    ('Motor Over Speed',                    1),
                    ('Active Motor index',                  13107),
                    ('Transmit error count',                51),
                    ('Receive error count',                 51)]




    specific_can_msg(test_list1, correct_list1) 
    specific_can_msg(test_list2, correct_list2)
    specific_can_msg(test_list3, correct_list3)
    specific_can_msg(test_list4, correct_list4)
    specific_can_msg(test_list5, correct_list5)
    specific_can_msg(test_list6, correct_list6)





def test_CANparse_IO_STATE():

    # Init Test Case 1
    #            |         CAN ID       |          IDX          |                     DATA                      |
    test_list1 = [0x00, 0x00, 0x05, 0x81, 0xFF, 0xFF, 0xFF, 0xFF, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
    #                                                          |63-56|55-48|47-40|39-32|31-24|23-16|15-08|07-00|
    correct_list1 = [("Accel Pedal",        0),
                    ("Brake Pedal",         0),
                    ("Switch Bitmap",       0),
                    ("Contactor Bitmap",    0)]


    # Init Test Case 2
    #            |         CAN ID       |          IDX          |                     DATA                      |
    test_list2 = [0x00, 0x00, 0x05, 0x81, 0xFF, 0xFF, 0xFF, 0xFF, 0x00, 0x00, 0x00, 0x00, 0xFF, 0xFF, 0xFF, 0xFF]
    #                                                          |63-56|55-48|47-40|39-32|31-24|23-16|15-08|07-00|
    correct_list2 = [("Accel Pedal",        255),
                    ("Brake Pedal",         255),
                    ("Switch Bitmap",       255),
                    ("Contactor Bitmap",    255)]


    # Init Test Case 3
    #            |         CAN ID       |          IDX          |                     DATA                      |
    test_list3 = [0x00, 0x00, 0x05, 0x81, 0xFF, 0xFF, 0xFF, 0xFF, 0x00, 0x00, 0x00, 0x00, 0x81, 0x81, 0x81, 0x81]
    #                                                          |63-56|55-48|47-40|39-32|31-24|23-16|15-08|07-00|
    correct_list3 = [("Accel Pedal",        129),
                    ("Brake Pedal",         129),
                    ("Switch Bitmap",       129),
                    ("Contactor Bitmap",    129)]

    # Run the Tests
    specific_can_msg(test_list1, correct_list1) 
    specific_can_msg(test_list2, correct_list2)
    specific_can_msg(test_list3, correct_list3)




def old2():

    # Init Test Case
    #           |         CAN ID       |          IDX          |                     DATA                      |
    test_list = [0x00, 0x00, 0x05, 0x81, 0xFF, 0xFF, 0xFF, 0xFF, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01]
    #                                                          |63-56|55-48|47-40|39-32|31-24|23-16|15-08|07-00|
    correct_list = [("Accel Pedal",         1),
                    ("Brake Pedal",         0),
                    ("Switch Bitmap",       0),
                    ("Contactor Bitmap",    0)]

    # Convert to Function's Prefered format
    canID = test_list[3::-1]
    idx = test_list[7:3:-1]
    data = test_list[16:7:-1]
    test_byteArray = bytearray(canID + idx + data)

    # Call the Function
    points_list = CANparse(test_byteArray)

    ############## Run the Tests ##############
    
    assert len(correct_list) == len(points_list)                                # Assert Point

    for i in range(len(points_list)):                     # Loop Through All Elements in Point List
        point = points_list[i]

        assert isinstance(point, Point)                                         # Assert Type
        #assert point.measurement == "IO_STATE"                                 # Assert Measrument
        assert point._fields == {correct_list[i][0]: correct_list[i][1]}        # Assert Field
        assert point._tags == {}                                                # Assert Tag


def old():

    # Init Test Case
    test_list =  [0x00, 0x00, 0x05, 0x81, 0xFF, 0xFF, 0xFF, 0xFF, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01]
    # Init Correct Output of Test Case
    correct_list = []

    # Make Test Message little Endiend
    canID = test_list[3::-1]
    idx = test_list[7:3:-1]
    data = test_list[16:7:-1]
    # Convert to Byte Array
    test_byteArray = bytearray(canID + idx + data)

    # Call the Function
    canOutput = CANparse(test_byteArray)

    ############## Run the Tests ##############
    output_point = canOutput[0]
    # Assert the type of the object
    assert isinstance(output_point, Point)

    # Assert the measurement name
    #assert output_point.measurement == "IO_STATE"

    # # Assert the fields
    assert output_point._fields == {"Accel Pedal": 1}

    # # Assert the tags
    assert output_point._tags == {}  # If there are no tags in your case
    
    # Assert the Field Data 
    assert canOutput[0]._fields.get('Accel Pedal') == 1



    # #for i in range(min(len(canOutput), len(correct_list))):
    # #    assert correct_list[i] == canOutput[i] 
