import os
import sys
import json
sys.path.append('C:/Users/Tarkuen/Python Projects/Hovedopgave/MVCHovedopgave/scrapy_mod/prot_82_scrapy')

from twisted.python import log
from twisted.internet import reactor, defer
from twisted.internet.task import deferLater
from twisted.internet.protocol import ServerFactory, ClientFactory, Protocol

from twisted.web.server import Site, NOT_DONE_YET
from twisted.web.resource import Resource

import prot_82_scrapy

# class PocServerFactory(http.HTTPFactory):
#     def buildProtocol(self, addr):
#         return PocServer()

class PocServerResource(Resource):
    isLeaf=True

    def __init__(self):
        self.command = 'cd ../scrapy_mod/prot_82_scrapy && scrapy crawl spider1'
        self.command = self.command + " -a url=https://www.dr.dk/presse/kontakt"
    
    def render_GET(self, request):
        deferred = defer.Deferred()
        #self.request=request
        deferred.addCallback(self.callback_crawl)
        deferred.addCallback(self.callback_render)
        #reactor.callLater(1, deferred.callback, "callback initiated")
        reactor.callInThread(deferred.callback, result=request)
        
        return NOT_DONE_YET
        
    def callback_render(self, result):
        with open('../scrapy_mod/prot_82_scrapy/output.json', 'r') as fil:
            line= fil.read().encode('utf-8')
        result.write(line)
        result.finish()
        # self.request.write(line)
        # self.request.finish()
    
    def callback_crawl(self, result, *args):
        os.popen(self.command).read()
        return result



# class PocServer(http.HTTPChannel):
#     requestFactory=PocServerResource

    # def __init__(self):
    #     

    # def dataReceived(self, data):
    #     deferred = defer.Deferred()
    #     log.msg('Data received {%s}' % data )

    #     

    #     os.popen(self.command).read()
    #     reactor.callLater(1, deferred.callback, "File Callback")
    #     deferred.addCallback(self.fileHandler)

    #     #deferred.addErrback(sys.exit())

    # def fileHandler(self, result):
    #     with open('../scrapy_mod/prot_82_scrapy/output.json', 'r') as fil:
    #         for l in fil.readlines():
    #             self.transport.write(l.encode('utf-8'))
    #         fil.close()
    #     print(result)

    # def connectionMade(self):
    #     log.msg('Client connection from {}'.format(self.transport.getPeer()))
        

    # def connectionLost(self, reason):
    #     log.msg('Lost connection because {}'.format(reason))

# def main():
#     log.startLogging(sys.stdout)
#     log.msg('Start your engines...')
#     reactor.listenTCP(16000, PocServerFactory())
#     #reactor.connectTCP('127.0.0.1', 16000)
#     reactor.run()

def main():
    log.startLogging(sys.stdout)
    log.msg('Start your engines...')
    reactor.listenTCP(16000, Site(PocServerResource()))
    #reactor.connectTCP('127.0.0.1', 16000)
    reactor.run()

if __name__ == "__main__":
    main()