"""Script taking input from user"""

import serial
import time

MAX_USER_INPUT_BUFFER_LENGTH = 512
SOCKET_PORT = 'port-two'
BAUDRATE = 9600

def check_for_input():
    """ Will take user input, checks if input does not exceed 512 characters
    This loop will execute for as long as input is invalid.
    Will return input through buffer variable
    """

    while True:
        input_buffer = input( "Please enter input here: " )
        if( len( input_buffer ) <= MAX_USER_INPUT_BUFFER_LENGTH ):
            return input_buffer
        else:
            print( "Current input exceeds maximum allowed characters." )

def send_data_over_serial( serial_port: serial.Serial, data_to_send: str ):
    """ This function takes input from the buffer in main, converts this to
    utf-8. The serial port is opened and the converted data will
    be written to it.
    """

    serial_port.write( bytes( data_to_send, 'ascii' ) )

def main():
    """Initialising a serial port object and setting the correct BAUD rate."""
    try:
        serial_port_object = serial.Serial(
            port=SOCKET_PORT,
            baudrate=BAUDRATE
        )

        while True:    #Executes an infinite loop, to repeat below functions
            main_buffer = check_for_input()
            send_data_over_serial( serial_port_object, main_buffer )

    except serial.SerialException as e:
        print( "Error configuring Serial port" )
        print( e )
    except Exception as e:
        print( "Failed to perform action" )
    #except KeyBoardInterrupt:
        serial_port.close()
        quit()





if __name__ == "__main__":
    main()
