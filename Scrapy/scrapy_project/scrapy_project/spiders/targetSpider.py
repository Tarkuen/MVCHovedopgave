from os import path

import scrapy as Scrapy
import collections, json, re

from scrapy_project.items import Email_Item

class TargetSpider(Scrapy.Spider):
    """
    Parameters:
    -----------
        Scrapy.Spider : Spider 
            Object passed to the function by the active Scrapy crawler.

        Attributes:
        -----------
        Name : String 
            Name of spider for command line execution

    Methods:
    -----------

        __init__
            lorem ipsum

        start_requests
            lorem ipsum

        parse
            lorem ipsum

    """
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
        """
        Overridden method from Spider super class. 
        Handles the results yielded by Scrapy.Downloader component.
        
        Parameters:
        -----------
        response : HTMLResponse 
            Object passed to the function by the active Scrapy crawler.

        Attributes:
        -----------
        @select : Scrapy.Selector
            Scrapy API to different HTML Selector libraries.
            This object uses the XPath implementation
        
        @item : Email_Item
            Item stores the result of our XPath search and it uses Scrapys own Item interface.
            It is created during the for loop over found HTML elements.

        @xpath_target : str
            Regular expression used to select relevant HTML elements with the 'select' attribute.
            Currently chooses the found e-mail address' ancestors div element or near paragraph item

        Returns:
        ----------
        Yields items :
        Items are picked up and stored in Scrapys Middleware object.
        These items are then stored in the 'output.json' file in the root directory.

        Scrapy Contract Test
        ----------
        
            @url https://www.dr.dk/presse/kontakt
            @scrapes emailAddress emailPage

        """
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