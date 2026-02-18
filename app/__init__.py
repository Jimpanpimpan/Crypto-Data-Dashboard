from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_security import Security, SQLAlchemyUserDatastore
from config import config  # dictionaryn


"""
STEP 3: app/__init__.py - Initialisera Flask-appen

Denna fil:
1. Skapar Flask-appen
2. Kopplar ihop alla extensions (database, login manager)
3. Registrerar blueprints (moduler för routes)
4. Skapar databastabeller

Denna fil är "hjärtat" i din applikation.
"""

# TODO 1: Importera vad du behöver
# - from flask import Flask
# - from flask_sqlalchemy import SQLAlchemy
# - from flask_login import LoginManager
# - from config import config
db = SQLAlchemy()
login_manager = LoginManager()
security = Security()

# TODO 2: Initiera extensions (utan app - vi gör det senare)
# Skapa två variabler:
# - db = SQLAlchemy()  (för databas)
# - login_manager = LoginManager()  (för login-system)


def create_app(config_name='development'):
    # inuti för att undvika circular imports
    from app.routes import main_bp, auth_bp, dashboard_bp
    from app.models import User, Role
    from app.forms import ExtendedRegisterForm

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security.init_app(app, user_datastore, register_form=ExtendedRegisterForm)

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)

    with app.app_context():
        db.create_all()

    return app

# TODO 3: Skapa funktionen create_app(config_name='development')
# Denna funktion:
#
# a) Skapa Flask-app: app = Flask(__name__)
#
# b) Ladda konfiguration: app.config.from_object(config[config_name])
#    (Detta läser från config.py baserat på vilket miljö vi använder)
#
# c) Initiera extensions med appen:
#    - db.init_app(app)
#    - login_manager.init_app(app)
#    - Sätt login_manager.login_view = 'auth.login'
#      (Omdirigerar till login-sidan om användare inte är inloggad)
#
# d) Importera blueprints: from app.routes import main_bp, auth_bp, dashboard_bp
#    (Vi skriver routes.py senare, men vi behöver förberedelse här)
#
# e) Registrera blueprints:
#    - app.register_blueprint(main_bp)
#    - app.register_blueprint(auth_bp)
#    - app.register_blueprint(dashboard_bp)
#
# f) Skapa databastabeller:
#    ```
#    with app.app_context():
#        db.create_all()
#    ```
#    (app_context säger till SQLAlchemy vilken app vi använder)
#
# g) Return app (returnera den skapade appen)


"""
TIPS:
- __name__ är ett speciellt namn som Flask använder för att veta var paketet är
- app_context() är viktigt om du gör databastuff utanför en request
- Blueprints är som "moduler" - de grupperar routes tillsammans
"""
