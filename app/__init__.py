from flask import Flask
from .api.v1 import v1


def create_app(config_setting):
    app = Flask(__name__)
    app.config.from_object(config_setting)

    app.register_blueprint(v1)

    return app
