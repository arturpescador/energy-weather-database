import psycopg2
from psycopg2 import sql
import json
import argparse
import datetime

import weather_api
import iea_api

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Database generator.')

    parser.add_argument('-f', '--fro', type=str, help='Starting date of the scrapping in format "%Y-%m-%d"')
    parser.add_argument('-t', '--to', type=str, help='Ending date of the scrapping in format "%Y-%m-%d"')
    parser.add_argument('-ts', '--time-step', type=int, help='Timestep of the queries in days')
    parser.add_argument('-db', '--database-name', type=str, help='Name of database in PostgreSQL', default='energy_weather_db')

    args = parser.parse_args()

    with open('db_config.json', 'r') as config_file:
        config = json.load(config_file)
        host = config['DB_HOST']
        username = config['DB_USER']
        password = config['DB_PASSWORD']

    conn = psycopg2.connect(host=host, user=username, password=password, dbname="postgres")
    conn.autocommit = True
    cur = conn.cursor()

    try:
        # Create new database
        cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(args.database_name)))
        print(f"Database {args.database_name} created successfully.")

        # Connect to new database
        cur.close()
        conn.close()
        conn = psycopg2.connect(host=host, user=username, password=password, dbname=args.database_name)
        conn.autocommit = True
        cur = conn.cursor()

        # Create weather table
        create_table_query = """
            CREATE TABLE Weather (
                id SERIAL PRIMARY KEY,
                location VARCHAR(100),
                temp INT,
                rh INT,
                feels_like INT,
                wx_phrase VARCHAR(100),
                valid_time_gmt VARCHAR(100)
            );
            """
        cur.execute(create_table_query)

        # Format date limits and time steps
        fro = datetime.datetime.strptime(args.fro, "%Y-%m-%d").date()
        to = datetime.datetime.strptime(args.to, "%Y-%m-%d").date()
        ts = datetime.timedelta(days=args.time_step)

        # Fill with weather data
        weather_api.database_maker.rdbms_maker(fro, to, ts, weather_api.weather_api.Location.NEW_YORK_CITY, cur)

        print("Table Weather created successfully.")

        # Create energy table
        create_table_query = """
            CREATE TABLE Energy (
                id SERIAL PRIMARY KEY,
                region VARCHAR(100),
                value REAL,
                date VARCHAR(100)
            );
            """
        cur.execute(create_table_query)

        # Fill with energy data
        iea_api.database_maker.rdbms_maker(fro, to, ts, iea_api.iea_api.Precision.HOURLY, iea_api.iea_api.Region.NEW_YORK, cur)

        print("Table Energy created successfully.")

    except psycopg2.Error as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the cursor and connection
        cur.close()
        conn.close()