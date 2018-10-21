import os
from flask import Flask

# Initialize application
my_app = Flask(__name__, static_folder="")

# app configuration
my_app_settings = os.getenv(
    'APP_SETTINGS',
    'my_app.config.DevelopmentConfig'
)
my_app.config.from_object(my_app_settings)

