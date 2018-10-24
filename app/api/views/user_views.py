from flask_restful import Resource, reqparse, marshal, fields
from app.api.models import users
from flask import jsonify, make_response
import random

users = users.Users.usersList()


class UsersAPI(Resource):
    def __init__(self):
        self.parse = reqparse.RequestParser()
        self.parse.add_argument('name', type=str, required=True,
                                help="Please add a name",
                                location='json'
                                )

        self.parse.add_argument('username', type=str,
                                default='user' +
                                str(random.randint(500, 5000)),
                                location='json'
                                )

        self.parse.add_argument('email', type=str,
                                required=True,
                                help="You are not \
                                    allowed here without email",
                                location='json'
                                )

        self.parse.add_argument('password', type=str,
                                required=True,
                                help='Please specify password',
                                location='json'
                                )

        super(UsersAPI, self).__init__()

    def get(self):
        return {
            'users': [marshal(user, user_fields)
                      for user in users]
        }

    def post(self):
        elements = self.parse.parse_args()

        user = {
            'name': elements['name'],
            'username': elements['username'],
            'email': elements['email'],
            'password': elements['password'],
            'user id': users[-1]['user id'] + 1
        }

        present = [userr for userr in users
                   if userr['email'] is elements['email']]

        if not present:
            users.append(user)

        else:
            return make_response(jsonify({'message':
                                         'That email is already registered'}),
                                 409)

        return {
            'Effect': 'Success. User added'
        }, 201


user_fields = {
    'name': fields.String,
    'email': fields.String,
    'username': fields.Integer,
    'password': fields.Boolean,
    'url': fields.Url('user id')
}
