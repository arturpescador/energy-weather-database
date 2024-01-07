# Description
Development of a basic framework for querying energy demand data from the IEA energy API, specifically targeting the dynamically displayed data accessible at the URL https://www.iea.org/data-and-statistics/data-tools/real-time-electricity-tracker.
# Usage
```python3
import iea_api
import datetime

# Define the starting date of the requested time series
start_date = datetime.date(2023, 11, 1)

# Define the ending date of the requested time series
end_date = datetime.date(2023, 11, 4)

# Define the chunk/page size, designed to allow several lighter payloads instead of one big payload
time_chunk = datetime.timedelta(days=1)

# Make requests to the IEA API for energy demand data
response = iea_api.database_maker.database_maker(
    start_date, 
    end_date, 
    time_chunk, 
    iea_api.iea_api.Precision.DAILY, 
    iea_api.iea_api.Region.NEW_YORK
)
```
