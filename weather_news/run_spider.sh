#!/bin/bash

# Run the Scrapy spider
scrapy crawl weather_spd

# Run the data processing script
python process_data.py -i weather_data.json -o weather_events.csv

