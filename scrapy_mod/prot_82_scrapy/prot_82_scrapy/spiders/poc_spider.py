import scrapy as Scrapy
import collections
from os import path

class PocSpider(Scrapy.Spider):
    name = 'spider1'

    def start_requests(self):
        #assert isinstance(urls, collections.Sequence)
        # urls= [
        #     'https://www.dr.dk/presse/kontakt',
        #     'https://www.prodata.dk/kontakt/adresse-og-medarbejdere/',
        # ]
        urls= [
           'https://webscraper.io/test-sites/e-commerce/allinone'
        ]
        for url in urls:
            yield Scrapy.Request(url=url,callback= self.parse)

    def parse(self, response):
        page = response.url.split('/')[-1]
        xpath_target="//a[contains(@href,'@')]/@href"
        # select = Scrapy.Selector(response=response)

        # xpath_target="//a[@href*='mail]"
        select = Scrapy.Selector(response=response)

        filename= 'output.txt'
        
        if path.isfile(filename):
            mode='a'
        else:
            mode = 'w'
        
        with open(filename, mode) as f:
            for link in select.xpath(xpath_target).getall():
                f.write(str(page)+' '+str(link ).strip('mailto:')+'\n')

        self.log('poc complete saved in %s' % filename)
