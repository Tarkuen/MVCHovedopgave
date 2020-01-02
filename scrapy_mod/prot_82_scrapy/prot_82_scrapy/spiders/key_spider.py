import scrapy as Scrapy
from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
import collections
import json
from os import path
import re


class KeySpider(CrawlSpider):
    name = 'spider3'
    rules=[
            Rule(LinkExtractor(allow=(r'/*')), callback='parse_item', follow=True),
        ]

    def __init__(self, url='', *args, **kwargs):
        super(KeySpider, self).__init__(*args, **kwargs)
        
        domain=str(url).split('//')[1].split('/')[0]
        self.allowed_domains = [domain,]
        self.start_urls = [str(url)+'/',]

    def parse_item(self, response):
        page = response.url.split('//')[1]
        xpath_target="//*[contains()]"
        select = Scrapy.Selector(response=response)
        filename= 'output.json'
        if len(select.xpath(xpath_target).getall()) == 0:
            return None

        with open(filename, 'a') as f:
            a = {}
            for link in select.xpath(xpath_target).getall():
                link= re.sub(r'(?:style/=)(?:.*)(?:/;/")' , "", link)
                a.update({str(link).strip('mailto:'):str(page)})
            f.write(json.dumps(a))
            f.close()

        self.log('emails appended to %s' % filename)
