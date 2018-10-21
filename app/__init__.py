
from flask import Flask

# Define the application object
my_app = Flask(__name__)

# Configurations
my_app.config.from_object('config')
