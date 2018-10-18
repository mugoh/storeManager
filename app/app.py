
from flask import Flask, jsonify


sales = [
    {
        'sales_record': 1,
        'attendant': u'Attendant One',
        'product': u'Spam 2.0',
        'quantity': u'1',
        'complete': False,
        'description': u'Hot with extra extra spam',
        'customer': {
            'name': u'Customer One',
            'address': u'45 bright street',
            'contact': [u'+00012345',
                        u'customer_one@example.co'
                        ]
        },
        'transaction type': u'Cash on Delivery',
        'gifts': None,
        'total for this sale': u'Ksh 276'
    },

    {
        'sales_record': 2,
        'attendant': u'Attendant Six',
        'product': u'Spam 2.0',
        'quantity': u'1',
        'complete': False,
        'description': u'Black with red eatable margins',
        'customer': {
            'name': u'Customer fifty',
            'address': u'42 bright street',
            'contact': [u'+00012345',
                        u'customer_c@example.co'
                        ]
        },
        'transaction type': u'Credit Card',
        'gifts':None,
        'total for this sale': u'Ksh 355'


    }

]
