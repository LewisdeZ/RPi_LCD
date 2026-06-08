#!/usr/bin/env python3

import openmeteo_requests

import pandas as pd
import requests_cache
from retry_requests import retry
from datetime import datetime
import zoneinfo
from utils import CyclicList


def get_response_openmeteo():
    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)

    # Make sure all required weather variables are listed here
    # The order of variables in hourly or daily is important to assign them correctly below
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": -37.814,
        "longitude": 144.9633,
        "daily": ["weather_code", "temperature_2m_max", "temperature_2m_min"],
        "hourly": "temperature_2m",
        "current": "temperature_2m",
        "timezone": "Australia/Sydney",
        "forecast_days": 2, # Ensure we don't run out of future hours...
    }
    responses = openmeteo.weather_api(url, params=params)

    return responses[0]


def get_weather():
    '''
    Get the current weather in Melbourne

    Returns:
        Dict containing two strings with keys:
            ['temp', 'weather_type']
            E.g. {'temp': '5° - 19° | 14°', 'weather': 'Overcast'}
    '''
    weather_codes = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Rime fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",
        56: "Freezing drizzle",
        57: "Freezing drizzle",
        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",
        66: "Freezing rain",
        67: "Freezing rain",
        71: "Slight snow",
        73: "Moderate snow",
        75: "Heavy snow",
        77: "Snow grains",
        80: "Slight showers",
        81: "Moderate showers",
        82: "Violent showers",
        85: "Snow showers",
        86: "Snow showers",
        95: "Thunderstorms",
        96: "Slight hail",
        97: "Moderate hail",
        98: "Moderate hail",
        99: "Heavy hail",
    }
    # Timezone info
    # TODO: Allow timezone to be passed as a variable
    tz = zoneinfo.ZoneInfo("Australia/Sydney")
    now = datetime.now(tz)
    current_hour = now.replace(minute=0, second=0, microsecond=0)

    # Get a resonse from the OpenMeteo API
    response = get_response_openmeteo()
    weather_dict = {} # {'hourly': {0: ..., 1: ...}, 'temp': {0: ..., 1: ...},...}

    # Process current data. The order of variables needs to be the same as requested.
    current = response.Current()
    current_temperature_2m = current.Variables(0).Value()

    # Process daily data. The order of variables needs to be the same as requested.
    daily = response.Daily()
    daily_weather_code = daily.Variables(0).ValuesAsNumpy()
    daily_temperature_2m_max = daily.Variables(1).ValuesAsNumpy()
    daily_temperature_2m_min = daily.Variables(2).ValuesAsNumpy()

    # Process the hourly data
    hourly = response.Hourly()

    #build a list of timezone-aware datetimes for each hourly temp slot
    start_ts = hourly.Time()
    interval = hourly.Interval()
    temps: np.ndarray = hourly.Variables(0).ValuesAsNumpy()

    num_entries = len(temps)
    slot_times = [
        datetime.fromtimestamp(start_ts + i * interval, tz=tz)
        for i in range(num_entries)
    ]

    # Find the index of the current hour
    current_index = next(
        (i for i, t in enumerate(slot_times) if t == current_hour), None
    )
    if current_index is None:
        raise ValueError(
            f"Current hour {current_hour} not found in forecast data. "
            f"Range: {slot_times[0]} - {slot_times[-1]}"
        )

    # TODO: Pass this as a variable in the function! It controls how many hours ahead to return...
    hours_ahead = 4
    # Slice: current hour + the requested number of future hours
    end_index = current_index + hours_ahead + 1
    selected_times = slot_times[current_index:end_index]
    selected_temps = temps[current_index:end_index]

    # E.g 10  11  12  13
    #     12° 15° 20° 25°
    weather_dict['hourly'] = {
        0: "".join(f"{selected_times[i].hour:<4}" for i in range(4)),
        1: "".join(f"{str(round(selected_temps[i]))+'°':<4}" for i in range(4)),
    }

    # Get a semi-readable temperature string
    # Formatted as f"{low}° - {high}° | {current}°"
    # E.g.          "5° - 15° | 12°"
    weather_dict['temp'] = {
        0: "LOW - HIGH | CUR",
        1: \
        f"{int(daily_temperature_2m_min[0]):>3}° - "\
        f"{int(daily_temperature_2m_max[0]):>3}°"\
        f"|{int(current_temperature_2m):>3}°"
                }

    # Get the simplified (short) weather string from dict defined above
    weather_dict['weather_type'] = {
        0: "WEATHER CODE:",
        1: weather_codes[daily_weather_code[0]]
    }


    return weather_dict

class Weather:
    def __init__(self):
        self.app_string={0: "", 1: ""}
        self.current_type = 'hourly' # Default view
        self.weather_menu_cycle = CyclicList(['hourly', 'temp', 'weather_type'])
        self.in_menu = True
        pass
    def __call__(self):
        '''
        Returns a dictionary with keys {0: ..., 1: ...}
        '''
        if self.in_menu:
            self.app_string[0] = "> " + self.weather_menu_cycle.getList()[0].replace("_", " ").upper()
            self.app_string[1] = self.weather_menu_cycle.getList()[1].replace("_", " ").upper()

        else:
            weather_dict = get_weather() # {'hourly': ..., 'temp': ..., 'weather_type'}
            self.app_string = weather_dict[self.current_type]

        return self.app_string

    # Handling button controls
    def _up(self):
        if self.in_menu:
            self.current_type = self.weather_menu_cycle.previous()
            self.app_string[0] = "> " + self.weather_menu_cycle.getList()[0].replace("_", " ").upper()
            self.app_string[1] = self.weather_menu_cycle.getList()[1].replace("_", " ").upper()
        return self.__call__()

    def _down(self):
        if self.in_menu:
            self.current_type = self.weather_menu_cycle.next()
            self.app_string[0] = "> " + self.weather_menu_cycle.getList()[0].replace("_", " ").upper()
            self.app_string[1] = self.weather_menu_cycle.getList()[1].replace("_", " ").upper()
        return self.__call__()

    def _left(self):
        # Return to weather home or back to main menu
        if self.in_menu:
            return None
        else:
            self.in_menu = True
            self.app_string[0] = "> " + self.weather_menu_cycle.getList()[0].replace("_", " ").upper()
            self.app_string[1] = self.weather_menu_cycle.getList()[1].replace("_", " ").upper()
            return self.__call__()

    def _right(self):
        self.in_menu = False
        return self.__call__()

    def _select(self):
        # Ensure the weather app returns to menu when select is pressed...
        self.in_menu = True


if __name__ == '__main__':
    weather_dict = get_weather()
    print(weather_dict['temp'])
    print(weather_dict['weather_type'])
    print(weather_dict['hourly'])

