from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_security import Security, SQLAlchemyUserDatastore
from config import config

db = SQLAlchemy()
login_manager = LoginManager()
security = Security()


def create_app(config_name='development'):
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
