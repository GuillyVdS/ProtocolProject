"""Script taking input from user"""

import serial
import time
import sys
from termios import TCIFLUSH, tcflush

MAX_USER_INPUT_BUFFER_LENGTH = 512
SOCKET_PORT = "port-two"
BAUDRATE = 9600
SERIAL_READ_TIMEOUT = 5

STX = int("AA", 16)
ETX = int("AB", 16)
EXE = int("AC", 16)


def check_for_input():
    """Will take user input, checks if input does not exceed 512 characters
    This loop will execute for as long as input is invalid.
    Will return input through buffer variable
    """

    while True:
        input_buffer = input("Please enter input here: ")
        if len(input_buffer) >= 1 and len(input_buffer) <= MAX_USER_INPUT_BUFFER_LENGTH:
            print("returning input buffer: \n")
            return input_buffer
        else:
            print(
                "Current input should be at least 1 character and should not exceed maximum allowed characters."
            )


def send_data_over_serial(serial_port: serial.Serial, data_to_send: bytearray):
    """This function takes input from the buffer in main, converts this to
    utf-8. The serial port is opened and the converted data will
    be written to it.
    """
    print("sending data: \n")
    serial_port.write(data_to_send)


def receive_data_over_serial(serial_port_receive: serial.Serial) -> bytearray:
    """This function takes a serial port object, retrieves information from the
    socket (in the form of bytes) and returns a decoded string.
    """

    while (data_received := serial_port_receive.read(512)) == b"":  # fmt: no
        print("timed out with no bytes")
        pass
    #newlist = []
    #for byte in data_received:
    #    newlist.append = byte.decode("ascii")
    #return newlist
    print("handling: ", data_received)
    return data_received
    #return data_received.decode("ascii")
    #result_in_string = ','.join(str(val) for val in data_received)
    #return result_in_string


def insert_exception_bytes(data_to_pack: bytearray):
    """This function takes a list of bytes of which it will scan for specific
    values. If a value matches any of the values it is looking for, an exception
    byte will be added. This is neccesary for the message not to conflict with
    any packet specific identifiers. """

    itr = enumerate(data_to_pack)
    for index, item in itr:
        if item == STX or item == ETX or item == EXE:
            data_to_pack.insert(index, EXE);
            next(itr)



def create_packet(data_to_pack: bytearray) -> bytearray:
    """This function takes a list of bytes to turn into a packet, runs the
    exception byte function and adds the start- and end bytes as well as a
    payload length.
    """

    insert_exception_bytes(data_to_pack)

    data_to_pack.insert(0, STX);
    payload_size = len(data_to_pack) - 1
    data_to_pack.insert(1, payload_size);
    data_to_pack.append(ETX);
    return data_to_pack

def unpack_packet(packet_to_unpack: bytearray ) -> bytearray:
    print("In function: " , packet_to_unpack)
    decoded_array = bytearray()
    exception_present = False
    print("test 121 ", packet_to_unpack)

    #string = str(packet_to_unpack)
    #print("Found " ,string)
    for byte in packet_to_unpack:
        print(byte)
        if exception_present == True:
            exception_present = False
            continue
        elif byte.decode("ascii") == ETX:
            break
        elif byte.decode("ascii") == EXE:
            exception_present = True
        else:
            decoded_array.append(byte)

    return decoded_array




def main():

    try:
        serial_port_object = serial.Serial(
            port=SOCKET_PORT, baudrate=BAUDRATE, timeout=SERIAL_READ_TIMEOUT
        )

        serial_port_object2 = serial.Serial(
            port="port-one", baudrate=BAUDRATE, timeout=SERIAL_READ_TIMEOUT
        )
        test_string = list("testABCtest")
        byte_array = bytearray("testABCtest", "ascii")
        byte_array.insert(5, STX )
        byte_array.insert(6, ETX)
        byte_array.insert(7, EXE )


        #serial_port_object.write(byte_array)
        print(byte_array)
        packet = create_packet(byte_array)
        print("test " , packet)
        send_data_over_serial(serial_port_object, packet)
        print("sent")
        packet_to_unpack =  receive_data_over_serial(serial_port_object2)
        print(packet_to_unpack)
        print(unpack_packet(packet_to_unpack))

        '''
        while True:  # Executes an infinite loop, to repeat below functions
            tcflush(sys.stdin, TCIFLUSH)
            main_buffer = check_for_input()
            send_data_over_serial(serial_port_object, main_buffer)
            print(receive_data_over_serial(serial_port_object))
'''
    except serial.SerialException as e:
        print("Error configuring Serial port")
        print(e)
    except Exception as e:
        print("Failed to perform action")
        # except KeyBoardInterrupt:
        serial_port.close()
        quit()


if __name__ == "__main__":
    main()
