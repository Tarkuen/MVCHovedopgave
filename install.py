import os, re, json, fileinput, random
from TwistedServer.configuration import Config


class InstallProject():

    def __init__(self):
        self.conf = Config()
        self.config_file = self.conf.getConfigDir()

    def replace_name(self, name_to_insert,target_file):
        name_to_insert = " name = '"+name_to_insert+"'\n"
        regex = r"(\sname = (?:.*)'\n)"
        for line in fileinput.input('Scrapy/scrapy_project/scrapy_project/spiders/'+target_file, inplace=True):
            line = re.sub(regex,name_to_insert,line, 1) if re.search(regex,line) else line
            print(line, end='')
        fileinput.close()

    def install(self):
        result = {}
        commands = self.conf.getCommands()
        defined_spiders = self.conf.getSpiders()
        
        for command in commands:
            value = input(f'Found server command: {command} . What query string should match it ? ')
            spidername = input(f'These spiders are available: {defined_spiders} \n Which Spider should {value} run? ')
            if value in result or spidername in result:
                print('A spider can only respond to one query string, and query strings must be unique. Aborting')
                break
            elif spidername not in defined_spiders:
                print('Name of spider script does not match any of the presented files. Aborting')
                break
            else:
                result.update({value:{command.strip('.py'):spidername}})

        [[self.replace_name(f'{j}', f'{k}') for (j,k) in i.items()] for i in result.values()]
        with open(self.config_file, 'w') as f:
            json.dump(result,f)


class HTMLGenerator():

    def __init__(self, keyword_dict):
        self.document="""
        <!DOCTYPE html>
        <html lang="en">
        <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta http-equiv="X-UA-Compatible" content="ie=edge">
        <link rel="stylesheet" type="text/css" href='style.css'>
        <title>Plugin</title>
        </head>
        <body class='pluginbody'>
        <div class='container'>
        <h1 class='text header'>Protendo Plugin</h1>
        <div>
        </div>
        """
        self.keywords_dict = keyword_dict
        self.keywords = self.keywords_dict.keys()
        self.logos = [
        'https://image.flaticon.com/icons/svg/2405/2405186.svg',
        'https://image.flaticon.com/icons/svg/1150/1150626.svg',
        'https://image.flaticon.com/icons/svg/122/122932.svg',
        'https://image.flaticon.com/icons/svg/2399/2399814.svg'
        ]

        self.document_location = (os.getcwd()+'\Google_Chrome_Extension\\init.html').replace('\\','/')
        self.item_name   = 'item'
        self.div_name    = 'actions'
        self.loader_name = 'container2'

    def createHTML(self):
        self.generateContainer(self.div_name)
        self.generateLoader(self.loader_name)
        self.document +="""
        <script src="popup.js"></script>
        </body>
        </html>
        """
        for line in fileinput.input(self.document_location, inplace=True):
            for line in self.document.split('\n'):
                print(line, end='')
        fileinput.close()
        print(f'Generated HTML in location : {self.document_location}')

    def generateLoader(self, loader_name):
        self.document+= f' \n </div> <div id="{loader_name}" class="{loader_name}"> \n'+ '<div id="act" class="lds-default act"> \n'
        for i in range(12):
            self.document += "<div></div>"
        self.document +"</div>\n"

    def generateContainer(self, class_name):
        self.document += f"<div class='{class_name}'>"
        self.openDiv(self.item_name)

    def openDiv(self, item_name):
        for keyword in self.keywords:
            self.document += f"<div class='{item_name}'> \n"
            self.document += self.openButton(keyword)
            self.document += f"</div> \n"

    def openButton(self, keyword):
        random_logo = self.logos.pop(random.randint(0, len(self.keywords)))
        button = f"<button id='{keyword}' class='text button'> "
        img = f'<img src="{random_logo}" height="50px" width="50px">{list(self.keywords_dict[keyword])[0]} '
        button += img +" </button>"
        return button

class JavaScriptGenerator():

    def __init__(self, keyword_dict):

        self.url = 'http://localhost:16000'
        self.document = """
            document.addEventListener("DOMContentLoaded", function() {
            var request_to_twisted = new XMLHttpRequest();
            var current_url;
            chrome.tabs.query({'active': true, 'lastFocusedWindow': true}, function (tabs) {
                current_url = tabs[0].url;
            });
            var loader = document.getElementById('container2');
        """
        self.keywords_dict = keyword_dict
        self.keywords = self.keywords_dict.keys()
        self.javascript_location = (os.getcwd()+'\Google_Chrome_Extension\\popup.js').replace('\\','/')
        self.document_location = (os.getcwd()+'\Google_Chrome_Extension\\response.html').replace('\\','/')


    def generateListenerEvent(self, url, element_id):
        self.document += f"\n \t document.getElementById('{element_id}').addEventListener('click', function()"+'{'
        self.document += '\n \t loader.style.display="block"; '
        self.document += f'\n \trequest_to_twisted.open("GET", "{url}?{element_id}="+current_url);'
        self.document += """
            request_to_twisted.onload = function() {
                if (request_to_twisted.status != 200) {
                    console.log('No connection could be made');
                }
                else {
                    loader.style.display="none"; \n 
                """
        self.document += 'chrome.tabs.create({"url": "file:///'+self.document_location+'"+"'+'?"+request_to_twisted.responseText}, function(tab) { });'+"}"+"};"
        self.document += '\n request_to_twisted.send("COMMIT"); }); \n'
    
    def initListeners(self):
        for keyword in self.keywords:
            self.generateListenerEvent(self.url ,keyword)
        self.document+= " });"

    def createJavaScript(self):
        self.initListeners()
        for line in fileinput.input(self.javascript_location, inplace=True):
            for line in self.document.split('\n'):
                print(line, end='')
        fileinput.close()
        print(f'Generated Javascript in location : {self.javascript_location}')
        

    def __str__(self):
        return f""" 
        JavaScriptGenerator values:
        {self.url}
        {self.document}
        {self.keywords_dict}
        {self.keywords}
        {self.javascript_location}
        {self.document_location}
        """
    

if __name__ == "__main__":
    install = InstallProject()
    install.install()
    keywords = install.conf.getConfig()
    htmlgen = HTMLGenerator(keywords)
    jsgen = JavaScriptGenerator(keywords)
    jsgen.createJavaScript()
    htmlgen.createHTML()
    import init_test
    init_test.create_test()
