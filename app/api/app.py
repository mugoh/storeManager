from flask import Flask, Blueprint
from flask_restful import Api
from views import product_views, sale_views

store_blueprint = Blueprint("store-man", __name__)


def create_app():
    my_app = Flask(__name__)
    api = Api(store_blueprint)

    api.add_resource(sale_views.SalesAPI,
                     '/stman/api/v1.0/sales', endpoint='sales')
    api.add_resource(product_views.ProductsAPI,
                     '/stman/api/v1.0/products', endpoint='products')
    api.add_resource(sale_views.SaleAPI,
                     '/stman/api/v1.0/sales/<int:sales_record>',
                     endpoint='sale')

    my_app.register_blueprint(store_blueprint)
    return my_app
