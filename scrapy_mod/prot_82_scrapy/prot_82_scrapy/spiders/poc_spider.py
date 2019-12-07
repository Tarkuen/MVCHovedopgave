import scrapy as Scrapy
import collections
from os import path
import json

class PocSpider(Scrapy.Spider):
    name = 'spider1'

    def __init__(self, url='', *args, **kwargs):
        super(PocSpider, self).__init__(*args, **kwargs)
        self.cURL = [url]  # py36
        print(self.cURL)

    def start_requests(self):
        
        for url in self.cURL:
            yield Scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split('//')[1]
        xpath_target="//a[contains(@href,'@')]/@href"
        # select = Scrapy.Selector(response=response)

        # xpath_target="//a[@href*='mail]"
        select = Scrapy.Selector(response=response)

        filename= 'output.json'
        
        if path.isfile(filename):
            mode='a'
        else:
            mode = 'w'
        
        with open(filename, 'w') as f:
            a = {}
            for link in select.xpath(xpath_target).getall():
                a.update({str(link).strip('mailto:'):str(page)})
            f.write(json.dumps(a))
            f.close()

        self.log('poc complete saved in %s' % filename)
