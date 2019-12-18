import scrapy as Scrapy
import collections
from os import path
import re
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
        xpath_target="//a[contains(@href,'@')]"
        select = Scrapy.Selector(response=response)
        filename= 'output.json'
        if len(select.xpath(xpath_target).getall()) == 0:
            self.log('no emails')
            return None
        
        # print(select.xpath(xpath_target).getall())
        # xpath_target="//a[contains(@href,'@')]/parent::p"
        # print(select.xpath(xpath_target).getall())
        xpath_target="//a[contains(@href,'@')]/ancestor::div/child::a | //a[contains(@href,'@')]/ancestor::div/child::p "
        # print(select.xpath(xpath_target).getall())
        
        with open(filename, 'w') as f:
            a = {}
            for link in select.xpath(xpath_target).getall():
                link= re.sub(r'(?:style/=)(?:.*)(?:/;/")' , "", link)
                a.update({str(link).strip('mailto:'):str(page)})
            f.write(json.dumps(a))
            f.close()

        self.log('emails appended to %s' % filename)
