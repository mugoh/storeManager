
class Sales:
    def __init__(self,
                 attendant, product, customer_name, quantity, price, date,
                 transaction_type):

        self.attendant = attendant
        self.customer_name = customer_name
        self.product = product
        self.price = price
        self.quantity = quantity
        self.date = date
        self.transaction_type = transaction_type
        self.id = 0
