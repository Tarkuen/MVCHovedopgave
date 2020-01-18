import os, re, json, fileinput
from TwistedServer.configuration import Config


class InstallProject():

    def __init__(self):
        self.conf = Config()
        self.config_file = 'TwistedServer/config.json'

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

if __name__ == "__main__":
    install = InstallProject()
    install.install()
    import init_test
    init_test.create_test()

