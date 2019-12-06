import scrapy as Scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
import collections
import json
from os import path

class PocSpider(Scrapy.spiders.CrawlSpider):
    name = 'spider2'

    def __init__(self, url='https://www.dr.dk/presse/kontakt', *args, **kwargs):
        super(PocSpider, self).__init__(*args, **kwargs)
        self.cURL = [url.strip("'")]  # py36
        self.allowed_domains = [self.cURL[0].split('//')[1].split('/')[0]+'/']
        self.start_urls = self.cURL
        print(self.allowed_domains)
        print(self.start_urls)
        rules=(
            Rule(LinkExtractor(), callback='parse_item', follow=True),
        )

    def parse_item(self, response):
        page = response.url.split('//')[1]
        xpath_target="//a[contains(@href,'@')]/@href"
        self.log('Parsing website')

        # xpath_target="//a[@href*='mail]"
        select = Scrapy.Selector(response=response)

        filename= 'output.json'
        
        if path.isfile(filename):
            mode='a'
        else:
            mode = 'w'
        
        with open(filename, 'w') as f:
            a = []
            for link in select.xpath(xpath_target).getall():
                a.append(str(link).strip('mailto:')+' : '+str(page))
            f.write(json.dumps(a))
            f.close()

        self.log('poc complete saved in %s' % filename)
