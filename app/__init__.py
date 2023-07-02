from flask import Flask
from flask_httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy

from config import Config


basic_auth = HTTPBasicAuth()
db = SQLAlchemy()


def create_app(class_config=Config):
    app = Flask(__name__)
    app.config.from_object(class_config)

    db.init_app(app)

    from app import api

    app.register_blueprint(api.blueprint, url_prefix='/api')

    return app


from app import models
