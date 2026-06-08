#!/usr/bin/env python3

from utils import CyclicList

class Settings:
    def __init__(self):
        self.app_string={0: "", 1: ""}
        self.current_setting = 'brightness' # Default setting
        self.settings_menu_cycle = CyclicList(['brightness', 'sleep_timeout'])
        self.in_menu = True
        pass
    def __call__(self):
        '''
        Returns a dictionary with keys {0: ..., 1: ...}
        '''
        if self.in_menu:
            self.app_string[0] = "> " + self.settings_menu_cycle.getList()[0].replace("_", " ").upper()
            self.app_string[1] = self.settings_menu_cycle.getList()[1].replace("_", " ").upper()
        else:
            # Getting settings...
            self.app_string = {0: "WORK IN", 1: "PROGRESS"}

        return self.app_string

    # Handling button controls
    def _up(self):
        if self.in_menu:
            self.current_type = self.settings_menu_cycle.previous()
            self.app_string[0] = "> " + self.settings_menu_cycle.getList()[0].replace("_", " ").upper()
            self.app_string[1] = self.settings_menu_cycle.getList()[1].replace("_", " ").upper()
        else:
            pass # Move setting up (previous) one
        return self.__call__()

    def _down(self):
        if self.in_menu:
            self.current_type = self.settings_menu_cycle.next()
            self.app_string[0] = "> " + self.settings_menu_cycle.getList()[0].replace("_", " ").upper()
            self.app_string[1] = self.settings_menu_cycle.getList()[1].replace("_", " ").upper()
        else:
            pass # Move setting down (next) one
        return self.__call__()

    def _left(self):
        # Return to settings home or back to main menu
        if self.in_menu:
            return None
        else:
            self.in_menu = True
            self.app_string[0] = "> " + self.settings_menu_cycle.getList()[0].replace("_", " ").upper()
            self.app_string[1] = self.settings_menu_cycle.getList()[1].replace("_", " ").upper()
            return self.__call__()

    def _right(self):
        self.in_menu = False
        return self.__call__()

    def _select(self):
        # Ensure the settings app returns to menu when select is pressed...
        self.in_menu = True
