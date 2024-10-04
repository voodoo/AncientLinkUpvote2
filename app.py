import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from sqlalchemy.orm import DeclarativeBase
from filters import timeago

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # Register the custom timeago filter
    app.jinja_env.filters['timeago'] = timeago

    with app.app_context():
        from models import User, Link, Comment, Vote
        db.create_all()

        from routes import main, auth, api
        app.register_blueprint(main.bp)
        app.register_blueprint(auth.bp)
        app.register_blueprint(api.bp)

    return app
