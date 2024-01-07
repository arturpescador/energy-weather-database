# Weather News Database

## Usage

### Running the Scrapy Spider

```bash
scrapy crawl weather_spd
```

### Running the Data Processing Script

```bash
python process_data.py -i weather_data.json -o weather_data.csv
```

### Running Both Scraping and Data Processing

```bash
chmod +x run_spider.sh
./run_spider.sh
```