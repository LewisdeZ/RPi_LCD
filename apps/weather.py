#!/usr/bin/env python3

import openmeteo_requests

import pandas as pd
import requests_cache
from retry_requests import retry
from datetime import datetime


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
        "forecast_days": 1,
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
    # Get a resonse from the OpenMeteo API
    response = get_response_openmeteo()
    weather_dict = {}

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

    hourly_data = {"date": pd.date_range(
        start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
        end =  pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
        freq = pd.Timedelta(seconds = hourly.Interval()),
        inclusive = "left"
    )}
    print(datetime.now().strftime("%H"))
    for hour in hourly_data['date']:
        print(hour)

    weather_dict['hourly'] = hourly.Variables(0).ValuesAsNumpy()

    # Get a semi-readable temperature string
    # Formatted as f"{low}° - {high}° | {current}°"
    # E.g.          "5° - 15° | 12°"
    weather_dict['temp'] = \
        f"{int(daily_temperature_2m_min[0])}° - "\
        f"{int(daily_temperature_2m_max[0])}°"\
        f" | {int(current_temperature_2m)}°"

    # Get the simplified (short) weather string from dict defined above
    weather_dict['weather_type'] = weather_codes[daily_weather_code[0]]

    return weather_dict

class Weather:
    def __init__(self):
        pass
    def __call__(self):
        weather_dict = get_weather()
        

if __name__ == '__main__':
    weather_dict = get_weather()
    print(weather_dict['temp'])
    print(weather_dict['weather_type'])
    print(weather_dict['hourly'])

