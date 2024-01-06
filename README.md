# Data Acquisition, Extraction and Storage Project

This project aims to develop a well-structured dataset.

## Structure

This repository is organized as follows:

- `iea_api`: Contains scripts for accessing the International Energy Agency's API for energy consumption data.

- `mapreduce/database_merger`: Includes scripts for merging datasets from different sources using MapReduce.

- `weather_api`: Scripts for fetching weather data from an external API.

- `weather_news`: Scripts used to scrape and process weather news data.

- `weather_scraper`: Scripts used to do web scraping and extract historical weather news data.

- `generate_iea.py`: A Python script to generate datasets from the IEA API.

- `generate_weather.py`: A Python script to generate weather-related datasets.

- `main.sh`: Main shell script to run the entire data acquisition pipeline.

- `merged_data.csv`: The resulting CSV file after merging weather and energy data.

- `quality_assessment.py`: Python script to assess the quality of merged datasets.

## Contributors

This project was developed by the following group members as part of the Data Aquisition, Extraction, and Storage at Université Paris Dauphine - PSL for the academic year 2023/2024:

- Artur Dandolini Pescador
- Caio Azevedo
- Jacques Xu
- Joseph Amigo

## Usage

```chmod +x ./energy-weather-database/main.sh && ./energy-weather-database/main.sh```
