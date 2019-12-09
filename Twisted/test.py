import os
import sys
import json
sys.path.append('C:/Users/Tarkuen/Python Projects/Hovedopgave/MVCHovedopgave/scrapy_mod/prot_82_scrapy')
import subprocess

from twisted.python import log
from twisted.internet import reactor, defer
from twisted.internet.task import deferLater
from twisted.internet.protocol import ServerFactory, ClientFactory, Protocol

from twisted.web.server import Site, NOT_DONE_YET
from twisted.web.resource import Resource

#import prot_82_scrapy

class PocServerResource(Resource):
    isLeaf=True

    # def __init__(self):
        
    #     # self.command = self.command + " -a url=https://www.dr.dk/presse/kontakt"
    
    def render_GET(self, request):
        command = 'cd ../scrapy_mod/prot_82_scrapy && scrapy crawl'
        log.msg('*'*15)
        for k in request.args:
            tmp = k.decode('utf-8')
            if tmp == 'target':
                command += f" spider1 -a url={str(request.args[k][0], 'utf-8')}"
            elif tmp == 'root':
                scheme = str(request.args[k][0], 'utf-8').split('//')[0]
                target = f"{scheme}//{str(request.args[k][0], 'utf-8').split('//')[1].split('/')[0]}"
                log.msg(target)
                command += f" spider2 -a url={target}"
        self.command=command
        log.msg(self.command)
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
        subprocess.call(self.command, shell=True)
        return result

def main():
    log.startLogging(sys.stdout)
    log.msg('Twisted Startet')
    reactor.listenTCP(16000, Site(PocServerResource()))
    reactor.run()

if __name__ == "__main__":
    main()