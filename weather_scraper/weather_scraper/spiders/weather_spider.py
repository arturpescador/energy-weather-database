import scrapy

class WeatherSpider(scrapy.Spider):
    name = 'weather_spider'
    allowed_domains = ['weatherapi.com']
    
    def start_requests(self):
        months = ['december', 'november', 'october', 'september', 'august', 'july', 'june', 'may', 'april', 'march', 'february', 'january']
        
        base_url = 'https://www.weatherapi.com/history/{month}/q/new-york-2618724'
        
        for month in months:
                # Construct the URL for each month of each year
                url = base_url.format(month=month)
                yield scrapy.Request(url, self.parse)
                
    def parse(self, response):
        # Extract the year and month from the URL or page content
        month = response.url.split('/history/')[-1].split('/')[0]
        
        # Navigate to the table body
        rows = response.xpath('//table[contains(@class, "table-bordered")]/tbody/tr')
        for row in rows:
            # Extract the text for each temperature data point
            day = row.xpath('.//td[1]/text()').get()
            min_temp = row.xpath('.//td[2]/text()').get()
            max_temp = row.xpath('.//td[3]/text()').get()
            avg_temp = row.xpath('.//td[4]/text()').get()

            # Yield a dictionary with the scraped data
            yield {
                'month': month,
                'year': day.strip() if day else day,
                'min_temp': min_temp.strip() if min_temp else min_temp,
                'max_temp': max_temp.strip() if max_temp else max_temp,
                'avg_temp': avg_temp.strip() if avg_temp else avg_temp
            }