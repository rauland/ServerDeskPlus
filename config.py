import configparser
from pathlib import Path

ini = Path("config.ini")
if not ini.is_file():
    config = configparser.ConfigParser()
    config['DEFAULT']={ 'url':''}
    config['email']= {}
    config['email']= {'username':'',
                    'mail_from':'',                    
                    'mail_to':'',
                    'at':'',}
                  
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

conf = configparser.ConfigParser()
conf.read('config.ini')

url = conf['DEFAULT']['url']
username = conf['email']['username']
mail_from = conf['email']['mail_from']
mail_to = conf['email']['mail_to']
at = conf['email']['at']
debug_flag = conf['email']['debug_flag']
message = conf['email']['message']