from flask import Blueprint, Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from app.api.v1.views import productv, salesv, userv


def create_app():
    jwt = JWTManager()

    app = Flask(__name__)
    app.config['JWT_SECRET_KEY'] = 'secrte.secrete'
    jwt.init_app(app)
    v1 = Blueprint('api', __name__, url_prefix='/api/v1.0')
    api = Api(v1)

    api.add_resource(productv.ProductList, '/products')
    api.add_resource(productv.ProductAPI, '/products/<int:id>')
    api.add_resource(salesv.SaleAPI, '/sales/<int:id>')
    api.add_resource(salesv.SalesList, '/sales')
    api.add_resource(userv.UsersList, '/users')
    # api.add_resource(userv.UserAPI, '/users/<int:id>')
    api.add_resource(userv.UserRegister, '/users/register')
    api.add_resource(userv.UserGiveAccess, '/users/access')
    api.add_resource(userv.UserLogout, '/users/logout/access')
    api.add_resource(userv.UserLogoutAnew, '/users/logout/refresh')

    app.register_blueprint(v1)

    return app
