from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask import redirect, request, url_for
from .config import Config
bootstrap = Bootstrap()
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)
    app.debug = True
    db.init_app(app)
    login_manager.init_app(app)

    from .auth import bp_auth
    app.register_blueprint(bp_auth, url_prfix="/")

    from .doctor import bp_doctor
    app.register_blueprint(bp_doctor, url_prfix='/doctor')

    from .hr import bp_hr
    app.register_blueprint(bp_hr, url_prfix="/hr")
    from .nurse import bp_nurse

    app.register_blueprint(bp_nurse, url_prfix="/nurse")
    from .patient import bp_patient

    app.register_blueprint(bp_patient, url_prfix="/patient")
    from .warehouse import bp_warehouse

    app.register_blueprint(bp_warehouse, url_prfix="/warehouse")

    return app
