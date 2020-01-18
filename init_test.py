from unittest import TestCase, TestSuite, TextTestRunner, TestLoader

import json, os, fileinput, re, socket, subprocess
from importlib import import_module


class SystemInitTest(TestCase):

    """ Folder and File dependencies-
    Conf.json , Output.json , Commands, Spiders
    Evt. Python Modules?
    """

    def setUp(self):
        self.config_file = '/TwistedServer/config.json'
        self.output_file = '/Scrapy/scrapy_project/output.json'
        self.command_dir = '/TwistedServer/commands'

    def confTestCase(self):
        """ Does conf.json exist? """
        print(os.getcwd())
        self.assertTrue(os.path.exists(os.getcwd()+self.config_file))
    
    def outputTestCase(self):
        """ Does output.json exist? """
        self.assertTrue(os.path.exists(os.getcwd()+self.output_file))
    
    def commandsTestCase(self):
        """ Does commands folder exist? """
        self.assertTrue(os.path.exists(os.getcwd()+self.command_dir))

    def runTest(self):
        self.setUp()
        self.confTestCase()
        self.outputTestCase()
        self.commandsTestCase()

class ScrapyTest(TestCase):

    """ Scrapy tests
    Spider namespace, Scrapy Items, parse_item regular expressions
    """
    def setUp(self):
        from TwistedServer.configuration import Config
        config = Config()
        self.conf_file_content = config.getConfig()
        self.name_regex = r"(\sname = '{}'\n)"
        self.style_regex = r'(?:style\=)(?:.*)(?:\;\")'
        self.command = 'cd Scrapy/scrapy_project && scrapy check '


    def spiderNameSpaceTestCase(self):
        """ Find conf.json names and match with spidernames """
        match = None
        for k,v in self.conf_file_content.items():

            values = list(v.items())

            spidername = values[0][0]
            spiderfile = values[0][1]
            for line in fileinput.input('Scrapy/scrapy_project/scrapy_project/spiders/'+spiderfile):
                tmp = re.search(self.name_regex.format(spidername),line)
                if tmp:
                    match = True
            self.assertTrue(match)
        
    
    def itemTestCase(self):
        """ Call scrapy check and evaluate response """
        self.assertEqual(subprocess.call(self.command, stdout=subprocess.PIPE, shell=True),1)

    def regularExpressionsTestCase(self):
        """ Test current regex in dummy file from /test/test.html """
        match = None
        with open('test/test.html', 'r') as f:
            for line in f.readlines():
                tmp = re.search(self.style_regex,line)
                if tmp:
                    match = True
        self.assertTrue(match)

    def runTest(self):
        self.setUp()
        self.spiderNameSpaceTestCase()
        self.regularExpressionsTestCase()


class TwistedTest(TestCase):

    """ Twisted Tests
    Port check.
    """

    def setUp(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def portTestCase(self):
        """ Testing if port 16.000 is taken """
        self.assertEqual(self.sock.connect_ex(('127.0.0.1',16000)),10061)
        
    def tearDown(self):
        self.sock.close()

    def runTest(self):
        self.setUp()
        self.portTestCase()
        self.tearDown()

def create_test():
    test_collection = TestSuite()
    test_collection.addTest(SystemInitTest())
    test_collection.addTest(ScrapyTest())
    test_collection.addTest(TwistedTest())
    TextTestRunner().run(test_collection)
