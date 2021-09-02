"""Script taking input from user"""

import serial
import time
import sys
from termios import TCIFLUSH, tcflush

MAX_USER_INPUT_BUFFER_LENGTH = 512
SOCKET_PORT = "port-two"
BAUDRATE = 9600
SERIAL_READ_TIMEOUT = 5

STX = 0xAA
ETX = 0xAB
EXE = 0xAC


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


def send_data_over_serial(serial_port: serial.Serial, data_to_send: str):
    """This function takes input from the buffer in main, converts this to
    utf-8. The serial port is opened and the converted data will
    be written to it.
    """
    print("sending data: \n")
    serial_port.write(bytes(data_to_send, "ascii"))


def receive_data_over_serial(serial_port_receive: serial.Serial) -> str:
    """This function takes a serial port object, retrieves information from the
    socket (in the form of bytes) and returns a decoded string.
    """

    while (data_received := serial_port_receive.read(512)) == b"":  # fmt: no
        print("timed out with no bytes")
        pass
    return data_received.decode("ascii")

def create_packet(data_to_pack: list):
    '''
    [] //len
    [] //payload
    [] //crc


    fun() <- add espae byte
    //iterators
    [] //sta\rt
    [] //end
    '''

    packet = [STX,0]
    size_of_payload = len(data_to_pack)
    for byte in data_to_pack:
        if byte == STX or byte == ETX or byte == EXE:
            packet.append(EXE)
            size_of_payload += 1
        packet.append(byte)
    packet[1] = size_of_payload
    packet.append(ETX)
    print(packet)

    for byte in packet:
        try:
            byte = ord(byte)
        except:
            print("nostring")
        print(byte)

    print(packet)




#def unpack_packet():


def main():

    test_string = list("testABCtest")
    test_string[7] = ETX
    test_string[2] = EXE
    test_string[8] = STX
    print(test_string)
    print(len(test_string))
    packet = create_packet(test_string)


    try:
        serial_port_object = serial.Serial(
            port=SOCKET_PORT, baudrate=BAUDRATE, timeout=SERIAL_READ_TIMEOUT
        )

        while True:  # Executes an infinite loop, to repeat below functions
            tcflush(sys.stdin, TCIFLUSH)
            main_buffer = check_for_input()
            send_data_over_serial(serial_port_object, main_buffer)
            print(receive_data_over_serial(serial_port_object))

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
