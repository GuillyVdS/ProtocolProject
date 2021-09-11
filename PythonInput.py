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
    serial_port.flush()


def receive_data_over_serial(serial_port_receive: serial.Serial) -> bytearray:
    """This function takes a serial port object, retrieves information from the
    socket (in the form of bytes) and returns a packet in the form of
    a byte array .
    """
    ReadByte = True
    while ReadByte == True:
        Current_Byte = serial_port_receive.read()
        print("Current B: " , Current_Byte)
        if Current_Byte == STX:
            print("GOT BYTE")





    #data_received = serial_port_receive.read(512)
    print("RECEIVING:" , data_received)
    #while ( data_received := serial_port_receive.read(512) ) == b"":  # fmt: no
        #print("timed out with no bytes")
        #pass

    return bytearray(data_received)

def insert_exception_bytes(data_to_pack: bytearray):
    """This function byte array of which it will scan for specific
    values. If a value matches any of the values it is looking for, an exception
    byte will be added. This is neccesary for the message not to conflict with
    any packet specific identifiers. """

    itr = enumerate(data_to_pack)
    for index, item in itr:
        if item == STX or item == ETX or item == EXE:
            data_to_pack.insert(index, EXE)
            next(itr)



def create_packet(data_to_pack: bytearray) -> bytearray:
    """This function takes a byte array to turn into a packet, runs the insert
    exception byte function and adds the start- and end bytes as well as a
    payload length.
    """

    insert_exception_bytes(data_to_pack)

    data_to_pack.insert(0, STX)             #start byte

    payload_size = len(data_to_pack) - 1    #payload size
    data_to_pack.insert(1, payload_size)

    data_to_pack.append(ETX)
                #end byte
    return data_to_pack




def unpack_packet(packet_to_unpack: bytearray ) -> bytearray:
    """Takes a byte array for the newly received packet. The first item in the
    array is deleted twice as to remove both the STX and the payload size.
    The ETX is stripped by deleting the last item in the array. (using -1)
    The enumerate cycles through every remaining item in the packet to check for
    any exception bytes to be removed.
    """

    del packet_to_unpack[0]
    del packet_to_unpack[0]
    del packet_to_unpack[-1]

    itr = enumerate(packet_to_unpack)
    for index, item in itr:
        if item == EXE:
            del packet_to_unpack[index]
            if packet_to_unpack[index] == EXE:
                next(itr)

def main():

    try:
        serial_port_object = serial.Serial(
            port=SOCKET_PORT, baudrate=BAUDRATE, timeout=2
        )

        serial_port_object2 = serial.Serial(
            port="port-one", baudrate=BAUDRATE, timeout=SERIAL_READ_TIMEOUT
        )
        test_string = "test0xABCtest"
        encoded_string = test_string.encode("ascii")

        byte_array = bytearray(encoded_string)
        #byte_array = bytearray("test0xABCtest", "ascii")
        byte_array.insert(5, STX )
        byte_array.insert(6, ETX)
        byte_array.insert(7, EXE )

        print(byte_array)
        packet = create_packet(byte_array)
        send_data_over_serial(serial_port_object, packet)
        print("sent")
        packet_to_unpack =  receive_data_over_serial(serial_port_object)
        print(packet_to_unpack)
        unpack_packet(packet_to_unpack)
        print(packet_to_unpack)
        print("test 123" ,packet_to_unpack.decode("ascii"))


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
