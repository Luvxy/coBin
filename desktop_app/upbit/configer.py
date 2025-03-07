import configparser
import os
from time import strftime

# 한번만 실행
def config_generator():
    if os.path.isfile('config.ini'):
        return
    
    # 설정파일 만들기
    config = configparser.ConfigParser()

    # 설정파일 오브젝트 만들기
    config['API'] = {}
    config['API']['access_key'] = ''
    config['API']['secret_key'] = ''
    config['API']['update'] = strftime('%Y-%m-%d %H:%M:%S')

    # 설정파일 저장
    with open('config.ini', 'w', encoding='utf-8') as configfile:
        config.write(configfile)


def config_read():
    
    # 설정파일 읽기
    config = configparser.ConfigParser()    
    config.read('config.ini', encoding='utf-8') 

    # 설정파일의 색션 확인
    # config.sections())
    return config
    
    
def config_edit(header, key, value):
    # 설정파일 읽기
    config = configparser.ConfigParser()    
    config.read('config.ini', encoding='utf-8') 

    # 설정파일의 색션 확인
    # config.sections())
    # version_read(config)
    config[header][key] = value
    with open('config.ini', 'w', encoding='utf-8') as configfile:
        config.write(configfile)


class strategy:
    def __init__(self, strategy_name, coin):
        self.strategy_name = strategy_name
        self.coin = coin

    def __str__(self):
        return f"{self.strategy_name} : {self.coin}"

    def __repr__(self):
        return f"{self.strategy_name} : {self.coin}"
    
    def save_strategy(self):
        pass