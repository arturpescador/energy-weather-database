import datetime
import time
import json
from .weather_api import *

MIN_DELTA = datetime.timedelta(days = 1)

RATE_PER_MINUTE = 30

def feature_handler(attr, val, location: Location):
    if attr == 'valid_time_gmt':
        return datetime.datetime.fromtimestamp(val, tz=location.tz).astimezone(datetime.timezone.utc).isoformat()

    return str(val)

def database_maker(fro: datetime.date, to: datetime.date, timestep: datetime.timedelta, location: Location):
    assert timestep >= MIN_DELTA, "timestep is smaller than the minimum timestep allowed by the weather API"
    while fro <= to:
        resp = get_weather_timeserie(fro, min(fro + timestep, to), location = location)
        fro += timestep + MIN_DELTA

        o = resp.json()['observations']
        for e in o:
            header = ['temp', 'rh', 'wc', 'feels_like', 'wx_phrase', 'valid_time_gmt']
            print(','.join([str(1)] + [location.id] + [feature_handler(attr, e[attr], location) for attr in header]), flush = True)

        time.sleep(60 / RATE_PER_MINUTE)
    return resp
