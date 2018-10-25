from flask_restful import Resource, reqparse, abort
from app.api.v1.models.users import Users, RevokeToken
import random
from passlib.hash import pbkdf2_sha256 as hash_pass
from flask_jwt_extended import (jwt_required, create_access_token,
                                get_raw_jwt, jwt_refresh_token_required)


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


def validate_inputs(element, input_arg):
    if not element:
        raise ValueError(
            f"Oops! {input_arg} is empty.\nPlease enter be a String")
    if isinstance(input, int):
        raise ValueError(
            f"Incorrect Detail {element}.\nTry making {input_arg} a String")
    return element


parse = reqparse.RequestParser()
parse.add_argument('name', type=validate_inputs, required=True,
                   help="Please add a name"
                   )

parse.add_argument('username', type=validate_inputs,
                   default='user' +
                   str(random.randint(500, 5000)),
                   location='json'
                   )

parse.add_argument('email', type=validate_inputs,
                   required=True,
                   help="You are not \
                            allowed here without email",
                        location='json'
                   )

parse.add_argument('password', type=validate_inputs,
                   required=True,
                   help='Please specify password'
                   )


class UserRegister(Resource):
    def post(self):
        email_form = re.compile(
            r"(^[a-zA-Z0-9_.-]+@[a-zA-Z-]+\.[.a-zA-Z-]+$)"
        )
        username_form = re.compile(r"(^[A-Za-z0-9-]+$)")

        elements = parse.parse_args()

        if len(elements['password']) < 6:
            abort(400,
                  message="Password too short. Make it at least 6\
            characters")

        if not re.match(email_form, elements['email']):
            abort(400, message="Email format not invented yet.\
            Try something like evil.cow@mammals.milk")

        if not re.match(username_form, elements['username']):
            abort(400, message="Try making \
                the username with just numbers and letters")

        found_users = [usr for usr in record_instance.user_records.values()]
        present = [usr for usr in found_users
                   if usr.email == elements['email']]

        # try:
        if not present:
            new_user = Users(
                name=elements['name'],
                email=elements['email'],
                username=elements['username'],
                password=Users.hashpasses(elements['password'])
            )
            u = elements['username']
            record_instance.post_record(new_user)
            return f'{u} created', 201

        else:
            abort(409, message="It's bad manners to register twice")

        # except:
        #    return "Oops! Something wrong happened", 500


class UserVerify:
    f_users = [usr for usr in record_instance.user_records.values()]

    def find_by_email(self, email):
            known_users = [usr for usr in f_users
                           if usr.email == email]

            return known_users[0]

    def verify_pass(self, password, email):
        known = [usr for usr in f_users
                 if usr.email == email]

        if not known:
            return False

        return hash_pass.verify(password, known['password'])


class UserGiveAccess(Resource):
    def post(self):
        elements = parse.parse_args()
        password = elements.get('password').strip()
        email = elements.get('email').strip()

        user = UserVerify.find_by_email(email)
        if not user:
            abort(401, message=f'{email} not known')

        if UserVerify.verify_pass(password, email):

            token = create_access_token(identity=user['name'])
            refresh_token = create_refresh_token(identity=user['name'])

            return "Login successful", 200

        else:
            abort(400, message="Oops, that didn't work. Try again?")


class UserLogout(Resource):
    @jwt_required
    def post(self):
        raw_jt = get_raw_jwt()['jti']

        try:
            revoked = RevokeToken(jti=raw_jt)
            revoked.add()

            return "Session revoked"
        except Exception as er:
            print(er)
            abort(500, message='Oops! Something bad happened')


class UserLogoutAnew(Resource):
    @jwt_refresh_token_required
    def post(self):
        raw_jt = get_raw_jwt()['jt']

        try:
            revoked = RevokeToken(jti=jti)
            revoked.add()
            return "Session revoked"
        except Exception as er:
            print(er)
            abort(500, message='Oops! Something bad happened')


class RefreshSession(Resource):
    pass


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
        alll = [user for user
                in record_instance.user_records.values()]

        return alll, 200
