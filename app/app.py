
from flask import Flask, abort

my_app = Flask(__name__, static_url_path="")

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
        'quantity': u'1',
        'date': datetime(2018, 6, 6, 5, 28, 56, 243),
        'description': u'Hot with extra extra spam',
        'transaction_type': u'Cash on Delivery',
        'complete': False,

        'gifts': 1,  # Anything to reduce sale e.g discounts
        'total': 276
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
        'quantity': u'1',
        'date': datetime(2018, 3, 16, 10, 3, 10, 7345),
        'description': u'Black with red eatable margins',
        'transaction_type': u'Credit',
        'complete': False,

        'gifts': 0,  # Any reduction in sale price
        'total': 355
    }

]




