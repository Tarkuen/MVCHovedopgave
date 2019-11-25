import scrapy as Scrapy
import collections

class PocSpider(Scrapy.Spider):
    name = 'spider1'

    def start_requests(self):
        #assert isinstance(urls, collections.Sequence)
        urls= [
            'https://www.prodata.dk/kontakt/adresse-og-medarbejdere/',
        ]
        for url in urls:
            yield Scrapy.Request(url=url,callback= self.parse)

    def parse(self, response):
        page = response.url.split('/')[-1]
        xpath_target="//a[@class= 'email']/@href"
        select = Scrapy.Selector(response=response)
       

        filename= 'output.txt'

        with open(filename, 'w') as f:
            for link in select.xpath(xpath_target).getall():
                f.write(str(page)+' '+str(link ).strip('mailto:')+'\n')

        self.log('poc complete saved in %s' % filename)
