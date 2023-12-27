import requests
import datetime
from enum import Enum

API_ENTRYPOINT = "https://api.iea.org/rte"

class Precision(Enum):
    WEEKLY = ("week", datetime.timedelta(weeks = 1))
    DAILY = ("day", datetime.timedelta(days = 1))
    HOURLY = ("hour", datetime.timedelta(hours = 1))

    def __init__(self, value, min_delta):
        self._value_ = value
        self.min_delta = min_delta

class Region(Enum):
    MID_ATLANTIC = "Mid-Atlantic"
    NEW_YORK = "New York"
    NEW_ENGLAND = "New England"
    CAROLINAS = "Carolinas"
    TENNESSEE = "Tennessee"
    MIDWEST = "Midwest"
    CENTRAL = "Central"
    TEXAS = "Texas"
    NORTHWEST = "Northwest"
    SOUTHWEST = "Southwest"
    CALIFORNIA = "California"

def get_demand_timeserie(fro: datetime.date, to: datetime.date, region: Region, precision: Precision):
    assert fro <= to, "fro must be before to"
    url = '/'.join([API_ENTRYPOINT, "demand", region.value, "timeseries"])
    params = {
        "from": fro.strftime("%Y-%m-%d"),
        "to": to.strftime("%Y-%m-%d"),
        "precision": precision.value,
        "region": True
    }
    return requests.get(url, params = params)
