from flask_restful import Resource, reqparse, abort
from app.api.models.users import Users
import random


class IntitalizeRecord:
    record = 0

    def __init__(self):
        self.user_records = {}

    def post_record(self, item):
        IntitalizeRecord.record += 1
        item.id = IntitalizeRecord.record
        self.user_records[IntitalizeRecord.record] = item

    def fetch_record(self, id):

        return self.user_records[id]


record_instance = IntitalizeRecord()


class UserAPI(Resource):
    @staticmethod
    def verify_existence(user_id):
        if user_id not in record_instance.user_records:
            reply = f'User {user_id} unknown.'

            abort(404, message=reply)

    def get(self, id):
        self.verify_existence(id)

        return record_instance.fetch_record(id)


class UsersList(Resource):
    def get(self):
        all = [user for user
               in record_instance.user_records.values()]

        return all

    def post(self):
        self.parse = reqparse.RequestParser()
        self.parse.add_argument('name', type=validate_inputs, required=True,
                                help="Please add a name",
                                location='json'
                                )

        self.parse.add_argument('username', type=validate_inputs,
                                default='user' +
                                str(random.randint(500, 5000)),
                                location='json'
                                )

        self.parse.add_argument('email', type=validate_inputs,
                                required=True,
                                help="You are not \
                                    allowed here without email",
                                location='json'
                                )

        self.parse.add_argument('password', type=validate_inputs,
                                required=True,
                                help='Please specify password',
                                location='json'
                                )
        elements = self.parse.parse_args()

        user = {
            'name': elements['name'],
            'username': elements['username'],
            'email': elements['email'],
            'password': elements['password'],
            'user id': users[-1]['user id'] + 1
        }

        present = [usr for usr in record_instance.user_records
                   if usr['email'] == elements['email']]

        if not present:
            record_instance.post_record(user)

            return user, 201

        else:
            abort(409, message="Email already registered")


def validate_inputs(input_arg, element):
    if not element:
        raise ValueError(
            f"Oops! {input_arg} is empty.\nPlease enter be a String")
    if isinstance(input, int):
        raise ValueError(
            f"Incorrect Detail {element}.\nTry making {input_arg} a String")
