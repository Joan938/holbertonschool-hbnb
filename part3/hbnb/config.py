import os

basedir = os.path.abspath(os.path.dirname(__file__))

class DevelopmentConfig:
    DEBUG = True
    SECRET_KEY = os.getenv('SECRET_KEY', 'my-secret-key')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'hbnb.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

config = {
    'default': DevelopmentConfig
}
