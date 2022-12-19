# Author: Phu Manh Nguyen
# Date: 12/17/2022

import os
import time

# Get an integer between min and max from user


def get_int(min, max, object) -> int:
    done = False
    while not done:
        try:
            user_int = int(input(f"Enter {object}: "))
        except ValueError:
            print("Invalid number. Please try again!")
        else:
            if user_int >= min and user_int <= max:
                done = True
            else:
                print(f"{object} must be between {min} and {max}")
    return user_int

# Clear the console after some seconds


def clean_console(second, message) -> None:
    print(message)
    time.sleep(second)
    os.system('cls')

# Get response (Y/N) from user


def get_response() -> str:
    response = input("Do you want to proceed? (Y/N) ")
    while (response not in ["Y", "N", "y", "n"]):
        print("Unrecognized command. Please try again!")
        response = input("Do you want to proceed? ")
    return response
