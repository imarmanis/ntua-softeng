from flask import Flask
from flask_cors import CORS
from config import Config


def create_app(config_class=Config):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)
    app.config.from_pyfile('config.py', silent=True)

    from app.models import db, ma, migrate
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    from app.resources import api
    api.init_app(app)
    CORS(app)
    return app
