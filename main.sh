( python ./generate_iea.py -f 2023-12-20 -t 2023-12-25 -ts 2; \
  python ./generate_weather.py -f 2023-12-20 -t 2023-12-25 -ts 2 ) | \
python ./mapreduce/database_merger/mapper.py | \
python ./mapreduce/database_merger/shuffler.py | \
python ./mapreduce/database_merger/reducer.py > merged_data.csv

python ./quality_assessment.py merged_data.csv
