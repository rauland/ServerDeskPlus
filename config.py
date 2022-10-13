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
                    'at':''}
                  
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

def get():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config