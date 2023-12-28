import iea_api
import datetime
fro = datetime.date(2023, 11, 1)
to = datetime.date(2023, 11, 5)
ts = datetime.timedelta(days = 2)
iea_api.database_maker.database_maker(fro, to, ts, iea_api.iea_api.Precision.DAILY, iea_api.iea_api.Region.NEW_YORK)
