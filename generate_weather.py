import weather_api
import datetime
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Weather database generator.')

    parser.add_argument('-f', '--fro', type=str, help='Starting date of the scrapping in format "%Y-%m-%d"')
    parser.add_argument('-t', '--to', type=str, help='Ending date of the scrapping in format "%Y-%m-%d"')
    parser.add_argument('-ts', '--time-step', type=int, help='Timestep of the queries in days')

    args = parser.parse_args()

    for location in weather_api.weather_api.Location:
        fro = datetime.datetime.strptime(args.fro, "%Y-%m-%d").date()
        to = datetime.datetime.strptime(args.to, "%Y-%m-%d").date()
        ts = datetime.timedelta(days = args.time_step)
        weather_api.database_maker.database_maker(fro, to, ts, location)
