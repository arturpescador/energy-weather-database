#cd spiders -> $scrapy crawl weather_spd
import scrapy
import json
import re

class WeatherSpider(scrapy.Spider):
    name = 'weather_spd'
    start_urls = ['https://www.weather.gov']

    def parse(self, response):
        data = {}

        areas = response.xpath('//map[@id="US_large_imagemap_800_500"]/area[string-length(substring-after(@href, "https://www.weather.gov/")) < 7]')

        for area in areas:
            title = area.xpath('@title').extract_first()
            href = area.xpath('@href').extract_first()
            

            if href.startswith('https://www.weather.gov/'):
                yield scrapy.Request(href, callback=self.parse_content, meta={'title': title, 'data': data})

    def parse_content(self, response):
        title = response.meta['title']
        data = response.meta['data']

        content = response.xpath('///*[@id="pagebody"]/div[1]/div[1]/p[1]/text()').get()

        climate_and_past_weather = response.xpath('//a[text()="Climate and Past Weather"]')
        sub_div = climate_and_past_weather.xpath('../following-sibling::div[@class="sub"]')
        vent_hrefs = sub_div.xpath('.//a[contains(., "vent")]/@href').extract()
        
        if vent_hrefs:
            data[title] = {'href': response.url, 'region': content, 'event_href': vent_hrefs, 'event_content':{}}
        else:
            data[title] = {'href': response.url, 'region': content}

        with open('weather_data.json', 'w') as json_file:
            json.dump(data, json_file, indent=4)

        self.log(f'Data for {title} saved in weather_data.json')

        for vent_href in vent_hrefs:
            yield scrapy.Request(vent_href, callback=self.parse_vent_content, meta={'title': title, 'data': data})

    def parse_vent_content(self, response):
        title = response.meta['title']
        data = response.meta['data']

        article_content = response.xpath("//text()").getall()

        data[title]['event_content'] =  article_content

        if title in data and 'event_hrefs' in data[title] and response.url in data[title]['event_hrefs']:
            data[title]['event_contents'][response.url] = article_content

        with open('weather_data.json', 'w') as json_file:
            json.dump(data, json_file, indent=4)

        self.log(f'Vent content for {title} saved in weather_data.json')
