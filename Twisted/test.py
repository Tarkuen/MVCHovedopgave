import os
import sys
import json
#sys.path.append('C:/Users/Tarkuen/Python Projects/Hovedopgave/MVCHovedopgave/scrapy_mod/prot_82_scrapy')

from twisted.python import log
from twisted.internet import reactor, defer
from twisted.internet.task import deferLater
from twisted.internet.protocol import ServerFactory, ClientFactory, Protocol

from twisted.web.server import Site, NOT_DONE_YET
from twisted.web.resource import Resource

#import prot_82_scrapy

class PocServerResource(Resource):
    isLeaf=True

    def __init__(self):
        self.command = 'cd ../scrapy_mod/prot_82_scrapy && scrapy crawl spider1'
        self.command = self.command + " -a url=https://www.dr.dk/presse/kontakt"
    
    def render_GET(self, request):
        deferred = defer.Deferred()
        deferred.addCallback(self.callback_crawl)
        deferred.addCallback(self.callback_render)
        reactor.callInThread(deferred.callback, result=request)
        
        return NOT_DONE_YET
        
    def callback_render(self, result):
        with open('../scrapy_mod/prot_82_scrapy/output.json', 'r') as fil:
            line= fil.read().encode('utf-8')
        result.write(line)
        result.finish()
    
    def callback_crawl(self, result, *args):
        os.popen(self.command).read()
        return result

def main():
    log.startLogging(sys.stdout)
    log.msg('Twisted Startet')
    reactor.listenTCP(16000, Site(PocServerResource()))
    reactor.run()

if __name__ == "__main__":
    main()