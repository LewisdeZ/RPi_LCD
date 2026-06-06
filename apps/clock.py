#!/usr/bin/env python3

import time
from datetime import datetime

class Clock:
    def __init__(self, ampm:bool=False):
        '''Clock utility.
        Args:
            ampm: If True, format time using am/pm formatting (else 24 hour)
        '''
        self.ampm=ampm

    def __call__(self):
        '''Get the current time as a dictionary

        Returns:
            Dict containing two strings with keys:
                ['0', '1'] (for lines 0 and 1 on display)
                if ampm == True, 'time' will contain a string with 'am' or 'pm' appended
                E.g.
                    ampm == True:
                        ['2024-05-09', '10:15PM']
                    ampm == False:
                        ['2024-05-09','22:15']
        '''
        # Get the current local date and time
        current_datetime = datetime.now()
        datetime_dict = {
            0: current_datetime.strftime("%Y-%m-%d")
        }

        # Get the current time (am/pm format else 24h)
        if self.ampm:
            datetime_dict[1] = current_datetime.strftime(
                "%I:%M%p"
            )
        else:
            datetime_dict[1] = current_datetime.strftime(
                "%H:%M"
            )

        return datetime_dict

    # Handling button controls
    def _up(self):
        self.ampm = not self.ampm
    def _down(self):
        self.ampm = not self.ampm
    def _left(self):
        pass
    def _right(self):
        pass


if __name__=='__main__':
    datetime_dict_24h = Clock(ampm=False)()
    print(f"24h datetime dict: \n\t{datetime_dict_24h}")

    datetime_dict_ampm = Clock(ampm=True)()
    print(f"AM/PM datetime dict:\n\t{datetime_dict_ampm}")
