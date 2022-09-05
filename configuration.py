from configparser import ConfigParser

config = ConfigParser()

config['default'] = {
    "token" : ""
}

with open("Telebot.ini", 'w') as f:
    config.write(f)