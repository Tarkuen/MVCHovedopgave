import os
import sys
import json
import subprocess
import config
import time
import asyncio

from twisted.python import log
from twisted.internet import reactor, defer, threads
from twisted.internet.task import deferLater
from twisted.internet.protocol import ServerFactory, ClientFactory, Protocol

from twisted.web.server import Request
from twisted.web.server import Site, NOT_DONE_YET
from twisted.web.resource import Resource


class ServerProtocol(Resource):
    """
    [[DESCRIPTION]]
    ...

    Attributes
    ----------


    Methods
    -------

    """

    isLeaf=True

    def __init__(self):
        super(Resource).__init__()
        conf = config.Config()
        self.spiders = conf.getConfig()

    
    def render_GET(self, request):
        """
        [[DESCRIPTION]]

        """

        command = 'cd ../scrapy_mod/prot_82_scrapy && scrapy crawl'
        print(f"Now Serving {request}")

        for k,v in self.spiders.items():
            if k in map(lambda x: x.decode('utf-8'), request.args):
                try:
                    command += getattr(self, str(v))(spidername=str(v),key=k, request=request, encoding='utf-8')
                    # cd ../scrapy_mod/prot_82_scrapy && scrapy crawl spider1 -a url=https://www.prodata.dk
                    self.command=command
                except AssertionError:
                    pass


        d = defer.Deferred()
        proc = subprocess.Popen(self.command, stdout=subprocess.PIPE, shell=True)
        request.processID=proc
        d.addCallback(self.recieveRequest)
        d.callback(request)
        request.notifyFinish().addErrback(self.requestHangUp,request)

        # crawl = defer.ensureDeferred(self.callback_crawl(d))
        # # d.addErrback(self.errorcode_handler)
        # d.callback(request)
        return NOT_DONE_YET

    def recieveRequest(self, requestObj):
        """  [[DESCRIPTION]]  """

        if requestObj.processID.poll() is None:
            return deferLater(reactor, 5,self.recieveRequest, requestObj)
        else:
            d = defer.Deferred()
            d.addCallback(self.handleResponse)
            d.callback(requestObj)

    def handleResponse(self,requestObj ):
        """  [[DESCRIPTION]]  """

        with open('../scrapy_mod/prot_82_scrapy/output.json', 'r') as fil:
            line= fil.read().encode('utf-8')
        print(f'renderering: {requestObj}')
        try:
            requestObj.write(line)
            requestObj.finish()
        except Exception:
            self.requestHangUp(Exception('Connection Closed'),requestObj)
        return requestObj
    

    def requestHangUp(self,err, item):
        """  [[DESCRIPTION]]  """

        item.processID.kill()
        print(f"Request Closed on {item}. Error is : {err}")


    def spider1(self, spidername,key,request,encoding):
        """  [[DESCRIPTION]]  """

        k = list(request.args.keys())[0]
        encoding=f"'{encoding}'"
        return f" {spidername} -a url={str(request.args[k][0], encoding)}"

    def spider2(self, spidername,key,request,encoding):
        """  [[DESCRIPTION]]  """
        
        k = list(request.args.keys())[0]
        encoding=f"'{encoding}'"
        scheme = str(request.args[k][0], encoding).split('//')[0]
        target = f"{scheme}//{str(request.args[k][0], encoding).split('//')[1].split('/')[0]}"
        return f" spider2 -a url={target}"


def main():
    log.startLogging(sys.stdout)
    log.msg('Twisted TCP Server Openened on port: 16000')
    reactor.listenTCP(16000, Site(ServerProtocol()))
    reactor.run()

if __name__ == "__main__":
    if os.path.exists('../scrapy_mod/prot_82_scrapy/output.json')==False :
        with open('../scrapy_mod/prot_82_scrapy/output.json', 'w') as f:
            pass

    main()