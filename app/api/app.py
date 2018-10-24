from flask import Flask, Blueprint
from flask_restful import Api
from views import product_views, sale_views
from instance.config import app_config

store_blueprint = Blueprint("store-man", __name__)


def create_app(config_setting):
    my_app = Flask(__name__)
    my_app.config.from_object(app_config[config_setting])
    api = Api(store_blueprint)

    api.add_resource(sale_views.SalesAPI,
                     '/stman/api/v1.0/sales', endpoint='sales')
    api.add_resource(product_views.ProductsAPI,
                     '/stman/api/v1.0/products', endpoint='products')
    api.add_resource(sale_views.SaleAPI,
                     '/stman/api/v1.0/sales/<int:sales_record>',
                     endpoint='sale')
    api.add_resource(product_views.ProductAPI,
                     '/stman/api/v1.0/products/<int:id>',
                     endpoint='product')

    my_app.register_blueprint(store_blueprint)
    return my_app
