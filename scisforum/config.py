import os
import json


#with open('/etc/config.json') as config_file:
#  config = json.load(config_file)


class Config:
    SECRET_KEY = '53ad147a12147000dc5eed019639856e'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'scisforum@gmail.com'
    MAIL_PASSWORD = 'f631c0873d4293dd'