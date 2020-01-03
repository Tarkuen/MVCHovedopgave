# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json

class Prot82ScrapyPipeline(object):
    def process_item(self, item, spider):
        self.itemExpo.update({item.get('emailAddress'): item.get('emailPage')})
        return item

    def open_spider(self, spider):
        self.file = open('output.json', 'w')
        self.itemExpo={}

    def close_spider(self,spider):
        self.itemExpo =  {x.replace('"',"'").replace("\\",""):y for x, y in self.itemExpo.items()}
        json.dump(self.itemExpo, self.file)
        self.file.close()