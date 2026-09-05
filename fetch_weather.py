import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry

def get_daily_weather(latitude=48.8833, longitude=2.5000, forecast_days=7):
    cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": ["temperature_2m_max", "temperature_2m_min", "precipitation_sum"],
        "timezone": "auto",
        "forecast_days": forecast_days,
    }
    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]
    daily = response.Daily()

    daily_data = {
        "date": pd.date_range(
            start=pd.to_datetime(daily.Time(), unit="s", utc=True),
            end=pd.to_datetime(daily.TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=daily.Interval()),
            inclusive="left"
        ),
        "temperature_max": daily.Variables(0).ValuesAsNumpy(),
        "temperature_min": daily.Variables(1).ValuesAsNumpy(),
        "precipitation_sum": daily.Variables(2).ValuesAsNumpy(),
    }
    return pd.DataFrame(data=daily_data)