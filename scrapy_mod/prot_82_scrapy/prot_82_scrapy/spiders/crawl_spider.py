import scrapy as Scrapy
from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
import collections
import json
from os import path


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
        print(self.allowed_domains)
        print(self.start_urls)

    def parse_item(self, response):
        page = response.url.split('//')[1]
        xpath_target="//a[contains(@href,'@')]/@href"
        select = Scrapy.Selector(response=response)
        filename= 'output.json'
        if len(select.xpath(xpath_target).getall()) == 0:
            return None
        
        if path.isfile(filename):
            mode='a'
        else:
            mode = 'w'
        
        with open(filename, mode) as f:
            a = {}
            for link in select.xpath(xpath_target).getall():
                a.update({str(link).strip('mailto:'):str(page)})
            f.write(json.dumps(a))
            f.close()

        self.log('emails appended to %s' % filename)
