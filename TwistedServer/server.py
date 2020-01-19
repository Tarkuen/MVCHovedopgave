import os, sys, json, subprocess,  time, asyncio
from importlib import import_module

from twisted.python import log
from twisted.internet import reactor, defer, threads
from twisted.internet.task import deferLater
from twisted.internet.protocol import ServerFactory, ClientFactory, Protocol
from twisted.web.server import Request, Site, NOT_DONE_YET
from twisted.web.resource import Resource

import configuration as config

class ServerProtocol(Resource):
    """ 
    Class for handling the HTTP protocol.
    The reactor listens for TCP connections and the Resource superclass interprets HTTP requetsts.

    Methods
    -------
        render_get
            Extension of superclass method 'render', which handles HTTP method calls.
            The suffix '_get' handles GET requests, as the name implies.

        recieveRequest
            Checks exit code of each request subprocess ID.
            If exit code is set, the function calls handleResponse.

        handleResponse
            Function for reading Scrapy output and sends it to the client.

        requestHangUp
            Function for handling TCP connection hang ups - Function kills subprocess.
    """

    isLeaf=True

    def __init__(self):
        super().__init__()

        self.command='cd ../Scrapy/scrapy_project && scrapy crawl'
        self.conf = config.Config()
        setattr(self.conf,'config_dir','config.json' )

        self.output_dir = self.conf.getOutputFile()
        self.spiders = self.conf.getConfig()

    def render_GET(self, request):
        command = self.command
        print(f"Now Serving {request}")

        for k,v in self.spiders.items():
            if k in map(lambda x: x.decode('utf-8'), request.args):
                try:
                    spidername = list(v.keys())[0]
                    mod_class= getattr(import_module(f'commands.{str(spidername)}'), f'{str(spidername)}')
                    command += getattr(mod_class, f'{str(spidername)}')(mod_class,spidername=str(spidername),key=k, request=request, encoding='utf-8')
                except Exception:
                    log.msg(f'{spidername} Module not found in {self.conf.command_dir}')

        if command == self.command:
            log.msg(f'Invalid keyword from request {request}')
            request.write(b'Invalid keyword. Check config.json for appropriate keywords')
            request.finish()
            return 1

        d = defer.Deferred()
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

    def handleResponse(self,requestObj ):

        with open(self.output_dir, 'r') as fil:
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

    main()
    
