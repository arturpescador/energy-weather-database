import weather_api
import datetime
fro = datetime.date(2023, 11, 1)
to = datetime.date(2023, 11, 5)
ts = datetime.timedelta(days = 2)
weather_api.database_maker.database_maker(fro, to, ts, weather_api.weather_api.Location.NEW_YORK_CITY)
