class spider2():

    def spider2(self,spidername,key,request,encoding):
        k = list(request.args.keys())[0]
        encoding=f"'{encoding}'"
        scheme = str(request.args[k][0], encoding).split('//')[0]
        target = f"{scheme}//{str(request.args[k][0], encoding).split('//')[1].split('/')[0]}"
        return f" {spidername} -a url={target}"

