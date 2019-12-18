import os
import sys
import json
# sys.path.append('C:/Users/Tarkuen/Python Projects/Hovedopgave/MVCHovedopgave/scrapy_mod/prot_82_scrapy')
import subprocess

from twisted.python import log
from twisted.internet import reactor, defer
from twisted.internet.task import deferLater
from twisted.internet.protocol import ServerFactory, ClientFactory, Protocol

from twisted.web.server import Site, NOT_DONE_YET
from twisted.web.resource import Resource

class PocServerResource(Resource):
    isLeaf=True
    
    def render_GET(self, request):
        command = 'cd ../scrapy_mod/prot_82_scrapy && scrapy crawl'
        if 'target' in map(lambda x: x.decode('utf-8'), request.args):
            command += f" spider1 -a url={str(request.args[b'target'][0], 'utf-8')}"
        else:   
            scheme = str(request.args[b'root'][0], 'utf-8').split('//')[0]
            target = f"{scheme}//{str(request.args[b'root'][0], 'utf-8').split('//')[1].split('/')[0]}"
            command += f" spider2 -a url={target}"
    
        self.command=command
        deferred = defer.Deferred()
        deferred.addCallback(self.callback_crawl)
        deferred.addCallback(self.callback_render)
        deferred.addErrback(self.errorcode_handler)
        reactor.callInThread(deferred.callback, result=request)
        
        return NOT_DONE_YET
        
    def callback_render(self, result):
        if hasattr(result,'resultcode'):
            log.msg(f"result errorcode: {result.returncode}")
        print(result)
        with open('../scrapy_mod/prot_82_scrapy/output.json', 'r') as fil:
            line= fil.read().encode('utf-8')
        result.write(line)
        result.finish()
    
    def callback_crawl(self, result, *args):
        try:
            subprocess.check_call(self.command, shell=True)
        except subprocess.CalledProcessError as e:
            log.msg(f"Exit Code: {e.returncode}")
            result.write(bytes(f"Exit Code: {e.returncode}", 'utf-8'))
            raise e
        return result

    def errorcode_handler(self,failure):
        # log.msg(f"Failure Object: {failure}")
        return 1


def main():
    log.startLogging(sys.stdout)
    log.msg('Twisted TCP Server Openened on port: 16000')
    reactor.listenTCP(16000, Site(PocServerResource()))
    reactor.run()

if __name__ == "__main__":
    if os.path.exists('../scrapy_mod/prot_82_scrapy/output.json')==False :
        with open('../scrapy_mod/prot_82_scrapy/output.json', 'w') as f:
            pass
    main()