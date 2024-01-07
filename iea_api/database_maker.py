import datetime
import time
import json
from .iea_api import *

RATE_PER_MINUTE = 30

def feature_handler(attr, val):
    if attr == 'Date':
        return val.replace(".000Z", "+00:00")

    return str(val)

def database_maker(fro: datetime.date, to: datetime.date, timestep: datetime.timedelta, precision: Precision, region: Region):
    assert timestep >= precision.min_delta, "timestep is smaller than the precision of the timeserie requested"
    while fro <= to:
        resp = get_demand_timeserie(fro, min(fro + timestep, to), region = region, precision = precision)
        fro += timestep + precision.min_delta

        o = resp.json()
        for e in o:
            header = list(e.keys())
            print(','.join([str(0)] + [feature_handler(attr, e[attr]) for attr in header]), flush=True)

        time.sleep(60 / RATE_PER_MINUTE)
    return resp

def rdbms_feature_handler(attr, val):
    if attr == 'Date':
        return val.replace(".000Z", "+00:00")

    return val

def rdbms_maker(fro: datetime.date, to: datetime.date, timestep: datetime.timedelta, precision: Precision, region: Region, cursor):
    assert timestep >= precision.min_delta, "timestep is smaller than the precision of the timeserie requested"
    while fro <= to:
        resp = get_demand_timeserie(fro, min(fro + timestep, to), region=region, precision=precision)
        fro += timestep + precision.min_delta

        o = resp.json()
        batch = []
        for e in o:
            header = list(e.keys())
            sample = [rdbms_feature_handler(attr, e[attr]) for attr in header]
            batch.append(sample)

        insert_query = """
            INSERT INTO Energy (region, value, date)
            VALUES (%s, %s, %s);
            """
        cursor.executemany(insert_query, batch)
