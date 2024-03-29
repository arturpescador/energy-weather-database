import requests
import datetime
import pytz
from enum import Enum

API_ENTRYPOINT = "https://api.weather.com/v1"
API_KEY = "e1f10a1e78da46f5b10a1e78da96f525"

class Location(Enum):
    NEW_YORK_CITY = ("KLGA:9:US", pytz.timezone("America/New_York"), "New York", "New York City")
    BUFFALO = ("KBUF:9:US", pytz.timezone("America/New_York"), "New York", "Buffalo")
    ROCHESTER = ("KROC:9:US", pytz.timezone("America/New_York"), "New York", "Rochester")
    YONKERS = ("KTEB:9:US", pytz.timezone("America/New_York"), "New York", "Yonkers")
    SYRACUSE = ("KSYR:9:US", pytz.timezone("America/New_York"), "New York", "Syracuse")
    ALBANY = ("KALB:9:US", pytz.timezone("America/New_York"), "New York", "Albany_NY")

    BURLINGTON_VT = ("KBTV:9:US", pytz.timezone("America/New_York"), "New England", "Burlington_VT")

    def __init__(self, value, tz, id, loc_str):
        self._value_ = value
        self.tz = tz
        self.id = id
        self.loc_str = loc_str

def get_weather_timeserie(fro: datetime.date, to: datetime.date, location: Location):
    assert fro <= to, "fro must be before to"
    url = '/'.join([API_ENTRYPOINT, "location", location.value, "observations", "historical.json"])
    resp = requests.get(url, params={
        "apiKey": API_KEY,
        "units": "h",
        "startDate": fro.strftime("%Y%m%d"),
        "endDate": to.strftime("%Y%m%d")
    })
    return resp
