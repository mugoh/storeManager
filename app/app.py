
from flask import Flask, abort, jsonify, make_response
from flask_restful import Api, fields, Resource, reqparse, marshal
from datetime import datetime
from flask_httpauth import HTTPBasicAuth

my_app = Flask(__name__, static_url_path="")
api = Api(my_app)
admin_auth = HTTPBasicAuth()
auth = HTTPBasicAuth()

sales = [
    {
        'sales_record': 1,
        'attendant': u'Attendant One',

        # Customer contacts
        'name': u'Customer One',
        'address': u'45 bright street',
        'contact': [u'+00012345', u'customer_c@example.co'],

        # Transaction Info
        'product': u'Spam 2.0',
        'quantity': 1,
        'date': datetime(2018, 6, 6, 5, 28, 56, 243),
        'description': u'Hot with extra extra spam',
        'transaction_type': u'Cash on Delivery',
        'complete': False,

        'gifts': 100,  # Anything to reduce sale e.g discounts
        'price': 276,
    },

    {
        'sales_record': 2,
        'attendant': u'Attendant Six',

        # Customer contacts
        'name': u'Customer fifty',
        'address': u'42 bright street',
        'contact': [u'+00012345', u'customer_c@example.co'],

        # Transaction Info
        'product': u'Spam 2.2',
        'quantity': 1,
        'date': datetime(2018, 3, 16, 10, 3, 10, 7345),
        'description': u'Black with red eatable margins',
        'transaction_type': u'Credit',
        'complete': False,

        'gifts': 0,  # Any reduction in sale price
        'price': 355
    }

]

products = [
    {
        'title': 'Bacon&Spam',
        'category': 'Hair Likes Food',
        'price': 934,
        'in stock': True,
        'date received': datetime(2018, 7, 10, 4, 2, 8, 564),
        'id': 1

    },

    {
        'title': 'Innocent Coconut Water',
        'category': 'Women sure can Sleep',
        'price': 94534,
        'in stock': True,
        'date received': datetime(
            2018, 5, 30, 22, 12, 38, 649),
        'id': 2
    }
]

# calculate total cost of each sale

for each_sale in sales:
    each_sale.update(
        {
            'total': each_sale.get('quantity') *
            each_sale.get('price') -
            each_sale.get('gifts')
        }
    )

product_fields = {
    'title': fields.String,
    'category': fields.String,
    'price': fields.Float,
    'in stock': fields.Boolean,
    'date received': fields.DateTime,
    'url': fields.Url('product')  # Ensure user doen't
                                  # need to know how to generate url
}

sale_fields = {
    'sales_uri': fields.Url('sale'),
    'attendant': fields.String,
    'gifts': fields.Integer,
    'price': fields.Fixed,
    'total': fields.Fixed
}

"""
    Output nested customer details
                                    """
sale_fields['customer'] = {}
sale_fields['customer']['Name'] = fields.String(attribute='name')
sale_fields['customer']['Address'] = fields.String(attribute='address')

# Create list for customer contacts
sale_fields['customer']['Contact'] = fields.List(
    fields.String, attribute='contact'
)


"""
    Nest the transaction info
                                    """

sale_fields['transaction_info'] = {}

sale_fields['transaction_info']['Product'] = fields.String(attribute='product')
sale_fields['transaction_info']['Quantity'] = fields.Integer(
    attribute='quantity'
)
sale_fields['transaction_info']['Date'] = fields.DateTime(
    attribute='date', dt_format='rfc822'
)
sale_fields['transaction_info']['Description'] = fields.String(
    attribute='description'
)
sale_fields['transaction_info']['Transaction_type'] = fields.String(
    attribute='transaction_type'
)
sale_fields['transaction_info']['Complete'] = fields.Boolean(
    attribute='complete'
)


admin_users = {
    'manager': 'man',
}

users = {
    'manager': 'man',
    'attendant': 'att'
}


@admin_auth.get_password
def use_password(username):
    if username in users:
        return admin_users.get(username)

    return None


@admin_auth.error_handler
def restricted():
    return make_response(jsonify({
        'message': "Access not allowed"
    }), 403
    )


@auth.get_password
def u_password(username):
    if username in users:
        return users.get(username)

    return None


@auth.error_handler
def restrict():
    return make_response(jsonify({
        'message': "Access not allowed"
    }), 403
    )


class AllSalesAPI(Resource):
    decorators = [auth.login_required]

    def __init__(self):

        """
        verify arguments' are in correct format
        """

        self.parse = reqparse.RequestParser()
        self.parse.add_argument('attendant', type=str,
                                required=True,
                                help="A sale need's an attendant",
                                location='json')

        # Customer details
        self.parse.add_argument('name', type=str,
                                default='Anonymous',
                                location='json')

        self.parse.add_argument('address', type=str,
                                default='Unknown',
                                location='json')

        self.parse.add_argument('contact', type=list,
                                default=['phone', 'email'],
                                location='json')

        # transaction details

        self.parse.add_argument('product', type=str,
                                required=True,
                                help="A product to sell sure has a name",
                                location='json')

        self.parse.add_argument('quantity', type=int,
                                help="How many items", default=1,
                                location='json')

        self.parse.add_argument('transaction_type', type=str,
                                default='Cash on Delivery',
                                location='json')

        self.parse.add_argument('gifts', type=int,
                                default='0',
                                location='json')

        self.parse.add_argument('price', type=int, required=True,
                                help="""You sure are not giving it away for free
                                """,
                                location='json')

        self.parse.add_argument('description', type=str,
                                default='',
                                location='json')

        super(AllSalesAPI, self).__init__()

    def get(self):
        return {
            'sales': [marshal(sale, sale_fields) for sale in sales]
        }

    def post(self):
        elements = self.parse.parse_args()

        sale = {
            'sales_record': sales[-1]['sales_record'] + 1,
            'attendant': elements['attendant'],
            'name': elements['name'],
            'address': elements['address'],
            'contact': elements['contact'],
            'product': elements['product'],
            'quantity': elements['quantity'],
            'date': datetime.now(),
            'description': elements['description'],
            'transaction_type': elements['transaction_type'],
            'complete': False,
            'gifts': 0,
            'price': elements['price']
        }

        # Find total cost of sale
        sale.update(
            {
                'total': sale.get('quantity') *
                sale.get('price') -
                sale.get('gifts')
            }
        )

        # Add new sale to sales record
        sales.append(sale)

        return {
            'sale': marshal(sale, sale_fields)
        }, 201


class SaleAPI(Resource):
    decorators = [admin_auth.login_required]

    """docstring for SaleAPI"""
    def __init__(self):
        self.parse = reqparse.RequestParser()
        self.parse.add_argument('attendant', type=str, location='json')
        self.parse.add_argument('transaction_info', type=dict, location='json')
        self.parse.add_argument('gifts', type=int, location='json')
        self.parse.add_argument('total',
                                type=float,
                                location='json'
                                )
        super(SaleAPI, self).__init__()

    def get(self, sales_record):
        sale = [sale for sale in sales if sale['sales_record'] == sales_record]

        if not sale:
            abort(404)

        return {'sale': marshal(sale[0], sale_fields)}

    def put(self, sales_record):
        sale = [sale for sale
                in sales if sale['sales_record'] is sales_record
                ]

        if not sale:
            abort(404)

        elements = self.parse.parse_args()

        # update any changed element
        for key, value in list(elements.items()):
            if value:
                sale[0][key] = value

        return {'sale': marshal(sale[0], sale_fields)}

    def delete(self, sales_record):
        sale = [sale for sale
                in sales if sale['sales_record'] is sales_record
                ]

        if not sale:
            abort(404)
        sales.remove(sale[0])

        return {
            'Effect': True
        }


class AllProductsAPI(Resource):
    """docstring for AllProductsAPI"""
    def __init__(self):
        self.parse = reqparse.RequestParser()
        self.parse.add_argument('title', type=str, required=True,
                                help="Please add a title",
                                location='json'
                                )

        self.parse.add_argument('category', type=str,
                                default='None',
                                location='json'
                                )

        self.parse.add_argument('price', type=int,
                                required=True,
                                help="You are not \
                                    allowed to give out stuff for free",
                                location='json'
                                )

        self.parse.add_argument('in stock', type=bool,
                                default=True,
                                location='json'
                                )

        super(AllProductsAPI, self).__init__()

    def get(self):
        return {
            'product': [marshal(product, product_fields)
                        for product in products]
        }

    @admin_auth.login_required
    def post(self):
        elements = self.parse.parse_args()

        product = {
            'title': elements['title'],
            'category': elements['category'],
            'price': elements['price'],
            'in stock': True,
            'date received': datetime.now(),
            'id': products[-1]['id'] + 1
        }

        products.append(product)

        return {
            'product': marshal(product, product_fields)
        }, 201


class ProductAPI(Resource):
    """docstring for ProductAPI"""
    def __init__(self):
        self.parse = reqparse.RequestParser()
        self.parse.add_argument('title', type=str,
                                location='json'
                                )

        self.parse.add_argument('category', type=str,
                                location='json'
                                )

        self.parse.add_argument('price', type=int,
                                location='json'
                                )

        self.parse.add_argument('in stock', type=bool,
                                location='json'
                                )

        super(ProductAPI, self).__init__()

    def get(self, id):
        product = [product for product in products if product['id'] is id]

        if not product:
            abort(404)

        return {
            'product': marshal(product[0], product_fields)
        }

    @admin_auth.login_required
    def put(self, id):
        product = [product for product in products if product['id'] is id]

        if not product:
            abort(404)
        elements = self.parse.parse_args()

        for key, value in list(elements.items()):
            if value:
                product[0][key] = value

        return {
            'product': marshal(product, product_fields)
        }

    @admin_auth.login_required
    def delete(self, id):
        product = [product for product in products if product['id'] is id]

        if not product:
            abort(404)
        product.remove(product[0])

        return {
            'Status': True
        }


api.add_resource(AllSalesAPI, '/stman/api/v1.0/sales', endpoint='sales')
api.add_resource(SaleAPI, '/stman/api/v1.0/sales/<int:sales_record>',
                 endpoint='sale'
                 )

api.add_resource(AllProductsAPI, '/stman/api/v1.0/products',
                 endpoint='products')
api.add_resource(ProductAPI, '/stman/api/v1.0/products/<int:id>',
                 endpoint='product')
