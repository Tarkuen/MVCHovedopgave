class CheckSite():

    def CheckSite(self,spidername,key,request,encoding):
        k = list(request.args.keys())[0]
        encoding=f"'{encoding}'"
        return f" {spidername} -a url={str(request.args[k][0], encoding)}"

