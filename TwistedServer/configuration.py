import json
class Config():

    def __init__(self):
        self.spiders={}
        with open('config.json', 'r') as f:
            data = json.load(f)

        for spider,value in data.items():
            self.spiders.update({spider:value})

    def getConfig(self):
        return self.spiders


    