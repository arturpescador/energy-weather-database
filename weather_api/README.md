# Description
Development of a basic framework for querying weather data from the weather.com API.
# Usage
```python
import weather_api
import datetime

# Define the starting date of the requested time series
start_date = datetime.date(2023, 12, 27)

# Define the ending date of the requested time series
end_date = datetime.date(2023, 12, 27)

# Define the chunk/page size, designed to allow several lighter payloads instead of one big payload
time_chunk = datetime.timedelta(days=2)

# Make requests to the weather API for weather data in New York City
response = weather_api.database_maker.database_maker(
    start_date, 
    end_date, 
    time_chunk, 
    weather_api.weather_api.Location.NEW_YORK_CITY
)
```
