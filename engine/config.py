import secrets


one_day = (60 * 60) * 24
class Config(object):
    DATABASE='./db/flaskr.sqlite'
    SESSION_TYPE = 'filesystem'
    SESSION_COOKIE_SECURE = True
    SESSION_USE_SIGNER = True
    SESSION_COOKIE_HTTPONLY = True
    PERMANENT_SESSION_LIFETIME = one_day
    APPLICATION_ROOT = '/'
    SESSION_PERMANENT = True

class DevConfig(Config):
    DEBUG = True
    DEVELOPMENT = True
    SECRET_KEY = 'dev'

class ProductionConfig(Config):
    DEBUG = False
    DEVELOPMENT = False
    SECRET_KEY = secrets.token_hex()
