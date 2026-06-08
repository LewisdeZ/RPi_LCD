#!/usr/bin/env python3

from utils import write_to_screen
from .cycle import CyclicList
import apps
import time


class MenuScreen():
    '''
    Class for selecting items in the menu screen
    '''
    def __init__(self, apps):
        self.all_apps = apps
        self.apps_cycle = CyclicList(self.all_apps)

        # If "in_app", controls will change things in the app...
        self.in_app = False

    def get_button_press(self, ser, button_press):
        # Handle button presses
        button_press = button_press.split(':')[-1]
        match button_press:
            case 'UP':
                self.up(ser)
            case 'DOWN':
                self.down(ser)
            case 'LEFT':
                self.left(ser)
            case 'RIGHT':
                self.right(ser)
            case 'SELECT':
                self.select(ser)

    def up(self, ser):
        if self.in_app:
            app_string = self.current_app['app']._up()
            write_to_screen(ser, app_string[0], 0)
            write_to_screen(ser, app_string[1], 1)
        else:
            self.current_app = self.apps_cycle.previous()
            # > CLOCK
            # WEATHER
            write_to_screen(ser, "> " + self.apps_cycle.getList()[0]['name'].upper(), 0)
            write_to_screen(ser, self.apps_cycle.getList()[1]['name'].upper(), 1)
        time.sleep(0.1)

    def down(self, ser):
        if self.in_app:
            app_string = self.current_app['app']._down()
            write_to_screen(ser, app_string[0], 0)
            write_to_screen(ser, app_string[1], 1)
        else:
            self.current_app = self.apps_cycle.next()
            # > CLOCK
            # WEATHER
            write_to_screen(ser, "> " + self.apps_cycle.getList()[0]['name'].upper(), 0)
            write_to_screen(ser, self.apps_cycle.getList()[1]['name'].upper(), 1)
        time.sleep(0.1)

    def left(self, ser):
        # Go up a the menu tree, or return home
        if self.in_app:
            app_string = self.current_app['app']._left()
            # App will return None if it wants to return home
            if app_string: # If it returns something, write it!
                write_to_screen(ser, app_string[0], 0)
                write_to_screen(ser, app_string[1], 1)
            else: # Else, write the home string menu, and set in_app to False
                self.in_app = False
                write_to_screen(ser, "> " + self.apps_cycle.getList()[0]['name'].upper(), 0)
                write_to_screen(ser, self.apps_cycle.getList()[1]['name'].upper(), 1)
        else:
            print("app_menu left")
        time.sleep(0.1)

    def right(self, ser):
        # Select menu option
        if self.in_app:
            app_string = self.current_app['app']._right()
            write_to_screen(ser, app_string[0], 0)
            write_to_screen(ser, app_string[1], 1)
        else:
            self.in_app = True
            app_string = self.current_app['app']()
            write_to_screen(ser, app_string[0], 0)
            write_to_screen(ser, app_string[1], 1)
            print(f"Current app: {self.current_app['name']}")
        time.sleep(0.1)

    def select(self, ser):
        # Swap between in_app=True and False
        if self.in_app:
            self.current_app['app']._select()
            # Reset to home...
            self.in_app = False
            write_to_screen(ser, "> " + self.apps_cycle.getList()[0]['name'].upper(), 0)
            write_to_screen(ser, self.apps_cycle.getList()[1]['name'].upper(), 1)
            print(f"Current app: home")
        else:
            print("Already at home...")

    def get_mode(self, ser):
        pass

if __name__=='__main__':
    apps = {
        "clock": apps.Clock(),
        # "weather": apps.Weather()
    }
