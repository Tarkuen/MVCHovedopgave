import os
import sys
sys.path.append('C:/Users/Tarkuen/Python Projects/Hovedopgave/MVCHovedopgave/scrapy_mod/prot_82_scrapy')

from twisted.python import log
from twisted.internet import reactor, defer
from twisted.internet.protocol import ServerFactory, ClientFactory, Protocol



import prot_82_scrapy

class PocServerFactory(ServerFactory):
    def buildProtocol(self, addr):
        return PocServer()


class PocServer(Protocol):

    def __init__(self):
        self.command = 'cd ../scrapy_mod/prot_82_scrapy && scrapy crawl spider1'

    def dataReceived(self, data):
        deferred = defer.Deferred()
        log.msg('Data received {%s}' % data )
        stdout = os.popen(self.command).read()
        deferred.addCallback(fileHandler(self.transport))

    def fileHandler(self, transport):
        with open('../scrapy_mod/prot_82_scrapy/output.txt', 'r') as fil:
            transport.write(fil.read().encode('utf-8'))
            fil.close()

    def connectionMade(self):
        log.msg('Client connection from {}'.format(self.transport.getPeer()))

    def connectionLost(self, reason):
        log.msg('Lost connection because {}'.format(reason))

def main():
    log.startLogging(sys.stdout)
    log.msg('Start your engines...')
    reactor.listenTCP(16000, PocServerFactory())
    #reactor.connectTCP('127.0.0.1', 16000)
    reactor.run()

if __name__ == "__main__":
    main()