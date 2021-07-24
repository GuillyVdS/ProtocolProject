#Script taking input from user

max_buffer_length = 512

# Will take user input, checks if input does not exceed 512 characters
def check_for_input():
    # This loop will execute for as long as input is invalid.
    # Will return
    while 1:
        buffer = input("Please enter input here: ")
        if(len(buffer) <= max_buffer_length):
            return buffer
        else:
            print("Buffer overflow")



def main():
    # Executes an infinite loop, to continiously execute below functions
    while 1:
        main_buffer = check_for_input()
        print('returning:', main_buffer)


if __name__ == "__main__":
    main()
