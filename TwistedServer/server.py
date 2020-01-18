import os, sys, json, subprocess,  time, asyncio
from importlib import import_module
from init_test import create_test

from twisted.python import log
from twisted.internet import reactor, defer, threads
from twisted.internet.task import deferLater
from twisted.internet.protocol import ServerFactory, ClientFactory, Protocol

from twisted.web.server import Request
from twisted.web.server import Site, NOT_DONE_YET
from twisted.web.resource import Resource

import configuration as config

class ServerProtocol(Resource):
    """
    [[DESCRIPTION]]
    ...

    Attributes
    ----------

    isLeaf : boolean
        lorem ipsum

    Methods
    -------
        render_get

        recieveRequest

        handleResponse

        requestHangUp
    """

    isLeaf=True

    def __init__(self):
        super(Resource).__init__()
        self.command='cd ../Scrapy/scrapy_project && scrapy crawl'
        conf = config.Config()
        setattr(conf,'config_dir','config.json' )
        self.spiders = conf.getConfig()

    def render_GET(self, request):
        command = 'cd ../Scrapy/scrapy_project && scrapy crawl'
        print(f"Now Serving {request}")

        for k,v in self.spiders.items():
            if k in map(lambda x: x.decode('utf-8'), request.args):
                try:
                    spidername = list(v.keys())[0]
                    mod_class= getattr(import_module(f'commands.{str(spidername)}'), f'{str(spidername)}')
                    command += getattr(mod_class, f'{str(spidername)}')(mod_class,spidername=str(spidername),key=k, request=request, encoding='utf-8')
                except Exception:
                    log.msg(f'Module not found. Check config.json for appropriate keywords')

        if command == 'cd ../Scrapy/scrapy_project && scrapy crawl':
            log.msg('Invalid keyword')
            request.write(b'Invalid keyword. Check config.json for appropriate keywords')
            request.finish()
            return 1

        d = defer.Deferred()
        # proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        request.processID=subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        d.addCallback(self.recieveRequest)
        request.notifyFinish().addErrback(self.requestHangUp,request)
        d.callback(request)

        return NOT_DONE_YET

    def recieveRequest(self, requestObj):

        if requestObj.processID.poll() is None:
            return deferLater(reactor, 2,self.recieveRequest, requestObj)
        else:
            self.handleResponse(requestObj)
            # d = defer.Deferred()
            # d.addCallback(self.handleResponse)
            # d.callback(requestObj)

    def handleResponse(self,requestObj ):

        with open('../Scrapy/scrapy_project/output.json', 'r') as fil:
            line= fil.read().encode('utf-8')
        print(f'renderering: {requestObj}')
        try:
            requestObj.write(line)
            requestObj.finish()
        except Exception:
            self.requestHangUp(Exception('Connection Closed'),requestObj)
        return requestObj
    

    def requestHangUp(self,err, item):

        item.processID.kill()
        print(f"Request Closed on {item}. Error is : {err}")

if __name__ == "__main__":
    def main():
        log.startLogging(sys.stdout)
        log.msg('Twisted TCP Server Openened on port: 16000')
        reactor.listenTCP(16000, Site(ServerProtocol()))
        reactor.run()

    create_test()
    main()
    
