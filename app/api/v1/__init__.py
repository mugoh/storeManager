from flask import Blueprint, Flask
from flask_restful import Api
from app.api.v1.views import productv, salesv, userv

app = Flask(__name__)
v1 = Blueprint('api', __name__, url_prefix='/api/v1.0')
api = Api(v1)

api.add_resource(productv.ProductList, '/products')
api.add_resource(productv.ProductAPI, '/products/<int:id>')
api.add_resource(salesv.SaleAPI, '/sales/<int:id>')
api.add_resource(salesv.SalesList, '/sales')
api.add_resource(userv.UsersList, '/users')
api.add_resource(userv.UserAPI, '/users/<int:id>')


app.register_blueprint(v1)
