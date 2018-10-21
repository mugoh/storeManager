import os
from flask import Flask

my_app = Flask(__name__)
#my_app.config.from_object(os.environ['APP_SETTINGS'])

my_app_settings = os.getenv(
    'APP_SETTINGS',
    'app.config.DevelopmentConfig'
)
my_app.config.from_object(my_app_settings)
