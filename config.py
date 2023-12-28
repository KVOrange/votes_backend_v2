"""Конфигурация программного обеспечения."""
import configparser

CONFIG_FILE = 'config.ini'
config = configparser.ConfigParser()
config.read(CONFIG_FILE)

SERVER_IP = config.get('SERVER', 'IP')
DOMEN = config.get('SERVER', 'DOMEN')
ADMIN_PATH = config.get('SERVER', 'ADMIN_PATH')

DATABASE_HOST = config.get('DATABASE', 'HOST')
DATABASE_USER = config.get('DATABASE', 'USER')
DATABASE_PASSWORD = config.get('DATABASE', 'PASSWORD')
DATABASE_NAME = config.get('DATABASE', 'NAME')