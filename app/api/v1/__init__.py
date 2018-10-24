from flask import Blueprint, Flask
from flask_restful import Api
from app.api.v1.views import productv

app = Flask(__name__)
v1 = Blueprint('api', __name__, url_prefix='/api/v1.0')
api = Api(v1)

api.add_resource(productv.ProductList, '/products')

app.register_blueprint(v1)
