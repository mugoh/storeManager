import os
from flask import Flask

my_app = Flask(__name__)
my_app.config.from_object(os.environ['APP_SETTINGS'])

return my_app

