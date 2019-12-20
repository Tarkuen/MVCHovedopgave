import scrapy as Scrapy
from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
import collections
import json
from os import path
import re


class PocSpider(CrawlSpider):
    name = 'spider2'
    rules=[
            Rule(LinkExtractor(allow=(r'/*')), callback='parse_item', follow=True),
        ]

    def __init__(self, url='', *args, **kwargs):
        super(PocSpider, self).__init__(*args, **kwargs)
        
        domain=str(url).split('//')[1].split('/')[0]
        self.allowed_domains = [domain,]
        self.start_urls = [str(url)+'/',]
        self.filename= 'output.json'
        with open(self.filename, 'w') as f:
            f.write('Currently no emails')

    def parse_item(self, response):
        page = response.url.split('//')[1]
        xpath_target="//a[contains(@href,'@')]"
        select = Scrapy.Selector(response=response)
        
        if len(select.xpath(xpath_target).getall()) == 0:
            return None

        with open (self.filename, 'r') as f:
            append=json.loads(f.read())
            
        with open(self.filename, 'w') as f:
            a = {}
            for link in select.xpath(xpath_target).getall():
                link= re.sub(r'(?:style\=)(?:.*)(?:\;\")' , "", link)
                a.update({str(link).strip('mailto:'):str(page)})
            append.update(a)
            json.dump(append, f)
            f.close()

        self.log('emails appended to %s' % self.filename)
