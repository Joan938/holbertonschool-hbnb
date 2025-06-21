import os

class Config:
    """
    Base configuration with default settings.
    """
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    DEBUG = False

class DevelopmentConfig(Config):
    """
    Development configuration: enables debug mode.
    """
    DEBUG = True

config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}