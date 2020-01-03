from os import path

import scrapy as Scrapy
import collections, json, re

from prot_82_scrapy.items import Email_Item

class TargetSpider(Scrapy.Spider):
    name = 'spider1'

    def __init__(self, url='', *args, **kwargs):
        super(TargetSpider, self).__init__(*args, **kwargs)
        self.cURL = [url]  # py36
        self.filename= 'output.json'
        self.xpath_target="//a[contains(@href,'@')]"
    def start_requests(self):
        
        for url in self.cURL:
            yield Scrapy.Request(url=url, callback=self.parse)
    
    def parse(self, response):
        select = Scrapy.Selector(response=response)
        if len(select.xpath(self.xpath_target).getall()) == 0:
            item=Email_Item(emailAddress="no emails",emailPage=f"{response.url.split('//')[1]}")
            return item

        xpath_target="//a[contains(@href,'@')]/ancestor::div/child::a | //a[contains(@href,'@')]/ancestor::div/child::p "
        for link in select.xpath(xpath_target).getall():
            link= re.sub(r'(?:style\=)(?:.*)(?:\;\")' , "", link)
            item=Email_Item(emailAddress=str(link).strip('mailto:'),emailPage=f"{response.url.split('//')[1]}")
            yield item

        self.log('emails appended to %s' % self.filename)