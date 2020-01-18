class rootSpider():

    def rootSpider(self,spidername,key,request,encoding):
        # url= ['https:', '', 'dr.dk', 'presse','kontakt']
        k = list(request.args.keys())[0]
        url = str(request.args[k][0], f"'{encoding}'").split('/')
        domain = url[2]
        fql = url[0]+'//'+domain
        return f" {spidername} -a url={fql} -a domain={domain}"