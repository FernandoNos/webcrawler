import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        allowed_domains=[
        'https://www.sicredi.com.br/']
        urls = [
           'https://www.sicredi.com.br/'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

     
    def parse(self, response):

        page = response.url.split("/")[-2]

        with open('output/'+page+'.txt', 'wb') as f:
            f.write('Page: '+page)
            print response.headers

            print response.headers['Content-Type']
            if 'text/html' in response.headers['Content-Type']:
                selectors =  response.selector.xpath('//a/@href')
                for selector in selectors:
                    url = selector.extract()
                    if 'http' in url:
                        f.write('  '+url+'\n')
                        #yield scrapy.Request(url, callback=self.parse)
            else:
                f.write( 'Static Document: '+response.url+'\n')
        f.close()

        
