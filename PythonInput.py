"""Script taking input from user"""

MAX_USER_INPUT_BUFFER_LENGTH = 512

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



def main():
    """Executes an infinite loop, to continiously execute below functions"""
    while True:
        main_buffer = check_for_input()
        print('returning:', main_buffer)


if __name__ == "__main__":
    main()
