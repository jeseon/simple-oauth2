import os

# Flask 환경 설정
class Config(object):
    DEBUG = False
    TESTING = False
    DEVELOPMENT = False
    JSON_AS_ASCII = False
    CSRF_ENABLED = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_POOL_RECYCLE = 7200
    SQLALCHEMY_DATABASE_URI = 'mysql://root:admin@localhost:3306/db?charset=utf8'
    SECRET_KEY = 'secret'


class ProductionConfig(Config):
    SECRET_KEY = 'production'


class StagingConfig(Config):
    DEBUG = True
    DEVELOPMENT = True


class DevelopmentConfig(Config):
    DEBUG = True
    DEVELOPMENT = True
    DEBUG_TB_PROFILER_ENABLED = True
    SQLALCHEMY_ECHO = True


class TestingConfig(Config):
    TESTING = True
    DEBUG_TB_PROFILER_ENABLED = True


def init_app(app):
    app.config.from_object({
        'testing': TestingConfig,
        'production': ProductionConfig,
        'development': DevelopmentConfig,
        'default': DevelopmentConfig
    }[os.getenv('FLASK_CONFIG', 'default')]())
