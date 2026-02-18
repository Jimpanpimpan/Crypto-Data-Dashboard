"""
STEP 1: config.py - Din applikations konfiguration

Denna fil lagrar ALLA inställningar som din Flask-app behöver.
Det gör det enkelt att byta inställningar utan att ändra koden på många ställen.
"""

import os

# ============================================================================
# TODO 1: Skapa en baseclass som heter 'Config'
# ============================================================================
# Denna class ska innehålla inställningar som gäller för ALL miljöer
# (development, production, testing)
#
# Vad du behöver lägga in:
# 1. SECRET_KEY - För att skydda användarens sessioner/cookies
#    - Använd: os.environ.get('SECRET_KEY') eller en default säker sträng
#    - TIPS: I development kan du sätta något enkelt som 'dev-secret-key-ändra-senare'
#
# 2. SESSION_COOKIE inställningar - För säkerhet
#    - SESSION_COOKIE_SECURE = False (vi använder inte HTTPS lokalt)
#    - SESSION_COOKIE_HTTPONLY = True (cookies bara via HTTP, inte JavaScript)
#    - SESSION_COOKIE_SAMESITE = 'Lax' (skyddar mot CSRF)
#
# 3. Database inställningar
#    - MYSQL_HOST = 'localhost'
#    - MYSQL_USER = 'root'
#    - MYSQL_PASSWORD = '' (vanligtvis tom på lokal MySQL)
#    - MYSQL_DB = 'crypto_dashboard'
#
# 4. SQLALCHEMY_DATABASE_URI - Anslutningssträngen för SQLAlchemy
#    - Format: 'mysql+pymysql://USER:PASSWORD@HOST/DATABASE'
#    - Exempel: 'mysql+pymysql://root:@localhost/crypto_dashboard'
#
# 5. SQLALCHEMY_TRACK_MODIFICATIONS = False (snabbare, vi behöver inte det)
#
# 6. COINGECKO_API_URL = 'https://api.coingecko.com/api/v3'
#    (Detta är APIet vi hämtar kryptodata från)


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-secret-key-ändra-senare"
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'  # Skydd mot CSRF, vad är det?

    # Database
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'user'
    MYSQL_PASSWORD = 'user123'
    MYSQL_DB = 'crypto_dashboard'

    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://user:user123@localhost/crypto_dashboard"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    COINGECKO_API_URL = 'https://api.coingecko.com/api/v3'

    WTF_CSRF_ENABLED = False

    # Flask-Security Configuration
    SECURITY_REGISTERABLE = True  # Enable registration
    SECURITY_SEND_REGISTER_EMAIL = False  # Don't require email confirmation
    SECURITY_PASSWORD_SALT = 'super-secret-password-salt-change-me'


class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False  # Varför Testing false?

# ============================================================================
# TODO 2: Skapa DevelopmentConfig class
# ============================================================================
# Denna ärver från Config (använd: class DevelopmentConfig(Config):)
# Lägg in:
# - DEBUG = True (så ser du felmeddelanden när något går fel)
# - TESTING = False


class ProductionConfig(Config):
    DEBUG = False  # Visa inte i fel produktionsserver
    TESTING = False
    SESSION_COOKIE_SECURE = True  # Använd HTTPS på produktionsserver

# ============================================================================
# TODO 3: Skapa ProductionConfig class
# ============================================================================
# Denna ärver från Config
# Lägg in:
# - DEBUG = False (säkerhetsskäl - visa inte fel på produktionsserver)
# - TESTING = False
# - SESSION_COOKIE_SECURE = True (använd HTTPS på produktionsserver)


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    # använder in-memory databas för tester
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


# ============================================================================
# TODO 4: Skapa TestingConfig class
# ============================================================================
# Denna ärver från Config
# Lägg in:
# - DEBUG = True
# - TESTING = True
# - SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:' (använd in-memory database för tests)


# ============================================================================
# TODO 5: Skapa en dictionary som mappar config-namn till classes
# ============================================================================
# Skapa dict som heter 'config' med:
# - 'development': DevelopmentConfig
# - 'production': ProductionConfig
# - 'testing': TestingConfig
# - 'default': DevelopmentConfig

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}


"""
VÄGLEDNING:
- Du kan använda os.environ.get('VARIABLE') för att läsa från miljövariabler
- Om miljövariabeln inte finns, ge en default-värde, t.ex:
  SECRET_KEY = os.environ.get('SECRET_KEY') or 'fallback-värde'

EXEMPEL på hur DATABASE_URI byggs:
  SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{user}:{password}@{host}/{database}'
"""
