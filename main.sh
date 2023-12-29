( python ./energy-weather-database/generate_iea.py -f 2023-12-20 -t 2023-12-25 -ts 2; \
  python ./energy-weather-database/generate_weather.py -f 2023-12-20 -t 2023-12-25 -ts 2 ) | \
python ./energy-weather-database/mapreduce/database_merger/mapper.py | \
python ./energy-weather-database/mapreduce/database_merger/shuffler.py | \
python ./energy-weather-database/mapreduce/database_merger/reducer.py
