import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from filters import timeago
from urllib.parse import urlparse

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
login_manager = LoginManager()
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
    }
    app.config['SECRET_KEY'] = os.urandom(24)

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    login_manager.login_view = 'auth.login'

    app.jinja_env.filters['timeago'] = timeago
    app.jinja_env.filters['urlparse'] = urlparse

    with app.app_context():
        from models import User, Link, Comment, Vote
        db.create_all()

        from routes import main, auth, api
        app.register_blueprint(main.bp)
        app.register_blueprint(auth.bp)
        app.register_blueprint(api.bp)

    return app
