import os

class Config:
    """
    Base configuration with default settings.
    """
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    DEBUG      = False

    # ─── Database ─────────────────────────────────────────────────────────────
    # Disable track modifications to save overhead
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Default to SQLite for development; override with DATABASE_URL in prod
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'sqlite:///dev.db'
    )

    # ─── JWT ────────────────────────────────────────────────────────────────────
    # Secret key for signing JWTs
    JWT_SECRET_KEY = SECRET_KEY


class DevelopmentConfig(Config):
    """
    Development configuration: enables debug mode.
    """
    DEBUG = True


config = {
    'development': DevelopmentConfig,
    'default':     DevelopmentConfig
}
