# Generate and Merge Data
( python ./generate_iea.py -f 2023-12-20 -t 2023-12-25 -ts 2; \
  python ./generate_weather.py -f 2023-12-20 -t 2023-12-25 -ts 2 ) | \
python ./mapreduce/database_merger/mapper.py | \
python ./mapreduce/database_merger/shuffler.py | \
python ./mapreduce/database_merger/reducer.py > energy_weather_related.csv

# Quality Assessment
python ./quality_assessment.py energy_weather_related.csv

# Create New Folder and Move File
mkdir -p dataset
mv energy_weather_related.csv dataset/

# Scrape Weather Data
cd weather_news
scrapy crawl weather_spd
python process_data.py -i weather_data.json -o weather_events.csv.csv

# Move the Weather Data CSV
mv weather_events.csv.csv ../dataset/

# Return to the original directory
cd ..

# Generate Relational Database (Needs db_config.json in root with psql credentials)
python ./generate_psql_db.py -f 2023-12-20 -t 2023-12-25 -ts 2
