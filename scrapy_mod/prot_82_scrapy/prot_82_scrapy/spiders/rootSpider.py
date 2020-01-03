from os import path
import collections, json, re

import scrapy as Scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from prot_82_scrapy.items import Email_Item


class RootSpider(CrawlSpider):
    name = 'spider2'
    rules=[
            Rule(LinkExtractor(allow=(r'/*')), callback='parse_item', follow=True),
        ]

    def __init__(self, url='', *args, **kwargs):
        super(RootSpider, self).__init__(*args, **kwargs)
        
        domain=str(url).split('//')[1].split('/')[0]
        self.allowed_domains = [domain,]
        self.start_urls = [str(url)+'/',]
        self.filename= 'output.json'
        self.xpath_target="//a[contains(@href,'@')]"

    def parse_item(self, response):
        select = Scrapy.Selector(response=response)
        
        if len(select.xpath(self.xpath_target).getall()) == 0:
            item=Email_Item(emailAddress="no emails",emailPage=f"{response.url.split('//')[1]}")
            return item
        self.xpath_target="//a[contains(@href,'@')]/ancestor::div/child::a | //a[contains(@href,'@')]/ancestor::div/child::p "

        for link in select.xpath(self.xpath_target).getall():
            link= re.sub(r'(?:style\=)(?:.*)(?:\;\")' , "", link)
            item=Email_Item(emailAddress=str(link).strip('mailto:'),emailPage=f"{response.url.split('//')[1]}")
            yield item

        self.log('emails appended to %s' % self.filename)
