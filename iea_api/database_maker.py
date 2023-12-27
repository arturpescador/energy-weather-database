import datetime
import time
import json
from .iea_api import *

RATE_PER_MINUTE = 30
def database_maker(fro: datetime.date, to: datetime.date, timestep: datetime.timedelta, precision: Precision, region: Region):
    assert timestep >= precision.min_delta, "timestep is smaller than the precision of the timeserie requested"
    while fro <= to:
        resp = get_demand_timeserie(fro, min(fro + timestep, to), region = region, precision = precision)
        fro += timestep + precision.min_delta
        
        o = resp.json()
        for e in o:
            header = list(e.keys())
            print(','.join([str(e[attr]) for attr in header]))

        time.sleep(60 / RATE_PER_MINUTE)
    return resp
