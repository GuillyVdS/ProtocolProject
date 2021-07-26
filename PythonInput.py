"""Script taking input from user"""

"""Importing the serial library to communicate over sockets, the time library
is used to add time delays"""

import serial
import time

MAX_USER_INPUT_BUFFER_LENGTH = 512
SOCKET_PORT = 'port-two'
BAUDRATE = 9600

"""Initialising a serial port object and setting the correct BAUD rate."""

ser = serial.Serial(
    port=SOCKET_PORT,
    baudrate=BAUDRATE
)


def check_for_input():
    """ Will take user input, checks if input does not exceed 512 characters
    This loop will execute for as long as input is invalid.
    Will return input through buffer variable
    """

    while True:
        input_buffer = input("Please enter input here: ")
        if(len(input_buffer) <= MAX_USER_INPUT_BUFFER_LENGTH):
            return input_buffer
        else:
            print("Current input exceeds maximum allowed characters.")

def send_data_over_serial(data_to_send):
    """ This function takes input from the buffer in main, converts this to
    utf-8. The serial port is opened and the converted data will
    be written to it.
    """

    data_as_bytes = bytes(data_to_send, 'utf-8')
    ser.close()
    ser.open()
    ser.write(data_as_bytes)
    time.sleep(3)
    print("Message has been sent")



def main():
    """Executes an infinite loop, to continiously execute below functions"""

    while True:
        main_buffer = check_for_input()
        send_data_over_serial(main_buffer)


if __name__ == "__main__":
    main()
