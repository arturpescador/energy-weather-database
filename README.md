# Data Acquisition, Extraction and Storage Project

This project aims to develop a well-structured dataset.

## Structure

This repository is organized as follows:

- dataset: Contains three data sets: `energy_weather_related.csv` , `weather_events.csv` and `Event_WeatherData.csv` ('Event_WeatherData.csv' is explained in the section of "Enrich weather news with weather measurement data" of the report)

- `iea_api`: Contains scripts for accessing the International Energy Agency's API for energy consumption data.

- `mapreduce/database_merger`: Includes scripts for merging datasets from different sources using MapReduce.

- `weather_api`: Scripts for fetching weather data from an external API.

- `weather_news`: Scripts used to scrape and process weather news data ; And the Scripts to generate TF-IDF index and inverted index with pyspark and MapReduce.

- `Merge_Dataset_NewAPI_and_WeatherNews`: Contains the scripts to generate `Event_WeatherData.csv` from ACIS Web Services API calls and `weather_data.csv`; Also contains inverted-index_table.csv and tfid_table.csv.

- `weather_scraper`: Scripts employed for web scraping and extracting historical weather data. Initially designed for scraping www.wunderground.com, we altered our approach, and ultimately, these scripts were not utilized in the final solution.

- `generate_iea.py`: A Python script to generate datasets from the IEA API.

- `generate_weather.py`: A Python script to generate weather-related datasets.

- `generate_psql_db.py`: A Python script to generate a PostgreSQL database with weather, energy and news data.

- `main.sh`: Main shell script to run the entire data acquisition pipeline.

- `merged_data.csv`: The resulting CSV file after merging weather and energy data.

- `quality_assessment.py`: Python script to assess the quality of merged datasets.


## Usage

To run the entire pipeeline, simply run the following command:

```chmod +x ./energy-weather-database/main.sh && ./energy-weather-database/main.sh```

This runs the entire pipeline, including the generation of the PostgreSQL database. For this reason it is necessary to have PostgreSQL credentials configured in a `db_config.json` file in the root directory.
