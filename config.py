import os
from dotenv import load_dotenv
load_dotenv()


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-secret-key-ändra-senare"
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'

    # Database
    MYSQL_HOST = os.environ.get('MYSQL_HOST')
    MYSQL_USER = os.environ.get('MYSQL_USER')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD')
    MYSQL_DB = os.environ.get('MYSQL_DB')

    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    COINGECKO_API_URL = 'https://api.coingecko.com/api/v3'
    COINGECKO_API_KEY = os.environ.get('COINGECKO_API_KEY')

    WTF_CSRF_ENABLED = False

    # Flask-Security Configuration
    SECURITY_REGISTERABLE = True  # Enable registration
    SECURITY_SEND_REGISTER_EMAIL = False  # Don't require email confirmation
    SECURITY_PASSWORD_SALT = 'super-secret-password-salt-change-me'


class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
