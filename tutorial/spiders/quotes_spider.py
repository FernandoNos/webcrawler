import scrapy
from scrapy import signals
from scrapy import Spider

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    allowed_domains=['www.sicredi.com.br']
    tree = {}
    count = 0
    root = None

    def start_requests(self):
        
        urls = [
           'https://www.sicredi.com.br/'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        self.count+=1
        print response.url
        if 'text/html' in response.headers['Content-Type']:
            selectors =  response.selector.xpath('//a/@href')
            for selector in selectors:
                url = selector.extract()
                if 'http' in url:
                    if self.allowed_domains[0] in url:
                        yield scrapy.Request(url, callback=self.parse)
        
