#!/usr/bin/env python3

import serial
import time

from apps import Clock, Weather
from utils import write_to_screen, MenuScreen

def main(menu_screen):
    write_to_screen(ser, 'READY!', 0)
    print("Ready for button inputs")
    while True:
        if ser.in_waiting:
            line = ser.readline().decode().strip()
            if line.startswith("BTN:"):
                menu_screen.get_button_press(ser, button_press=line)


if __name__ == '__main__':
    # Set up the arduino serial port
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    time.sleep(1)  # wait for Arduino reset

    # Define an apps dictionary that contains the apps and their names
    apps = []

    # Add the apps to the dictionary
    apps.append({"name": "clock", "app": Clock()})
    apps.append({"name": "weather", "app": Weather()})

    # Create the menu screen tool
    menu_screen = MenuScreen(apps)

    main(menu_screen)
