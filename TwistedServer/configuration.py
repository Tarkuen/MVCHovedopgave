import json, os, re

class Config():

    def __init__(self):
        self.spiders={}
        self.config_dir  = 'TwistedServer/config.json'
        self.command_dir = 'TwistedServer/commands'
        self.spiders_dir = 'Scrapy/scrapy_project/scrapy_project/spiders'

    def getConfig(self):
        with open(self.config_dir, 'r') as f:
            data = json.load(f)

        for spider,value in data.items():
            self.spiders.update({spider:value})
        return self.spiders

    def getSpiders(self):
        spider_files = set(os.listdir(self.spiders_dir))
        temp = set([])
        [ temp.add(entry) for entry in spider_files if re.match(r'(__.*__.py)|(__.*__)', entry) ]
        return set.symmetric_difference(spider_files,temp)

    def getCommands(self):
        files  = set(os.listdir(self.command_dir))
        temp = set([])
        [ temp.add(entry) for entry in files if re.match(r'(__.*__.py)|(__.*__)', entry) ]
        return set.symmetric_difference(files, temp)
