#!/usr/bin/env python3

from utils import write_to_screen
from .cycle import Cycle
import apps
import time


class MenuScreen():
    '''
    Class for selecting items in the menu screen
    '''
    def __init__(self, apps):
        self.all_apps = apps
        self.apps_cycle = Cycle(self.all_apps)
        self.in_app = False # If "in_app", controls will change things in the app...
        self.current_app = {"name": "home", "app": None}

    def get_button_press(self, ser, button_press):
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
            print("in_app up")
            pass
        else:
            self.current_app = self.apps_cycle.next()
            write_to_screen(ser, self.current_app["name"], 1)
            pass
        time.sleep(0.1)
    def down(self, ser):
        if self.in_app:
            print("in_app down")
            pass
        else:
            self.current_app = self.apps_cycle.previous()
            write_to_screen(ser, self.current_app["name"], 1)
            pass
        time.sleep(0.1)
    def left(self, ser):
        if self.in_app:
            print("in_app left")
            pass
        else:
            print("app_menu left")
            pass
        write_to_screen(ser, 'LEFT', 1)
        time.sleep(0.1)
    def right(self, ser):
        if self.in_app:
            print("in_app right")
            pass
        else:
            print("app_menu right")
            pass
        write_to_screen(ser, 'RIGHT', 1)
        time.sleep(0.1)
    def select(self, ser):
        if self.in_app:
            print("in_app select")
        else:
            print("app_menu select")

    def get_mode(self, ser):
        pass

if __name__=='__main__':
    apps = {
        "clock": apps.Clock(),
        # "weather": apps.Weather()
    }
