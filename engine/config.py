import secrets


class Config(object):
    DATABASE='./db/flaskr.sqlite'

class DevConfig(object):
    DEBUG = True
    DEVELOPMENT = True
    FLASK_SECRET = 'dev'

class ProductionConfig(Config):
    DEVELOPMENT = False
    DEBUG = False
    FLASK_SECRET = secrets.token_hex()
