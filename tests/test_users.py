import unittest
from run import create_app
import json
import sys

my_app = create_app()


class BasicUsersTests(unittest.TestCase):
    def setUp(self):
        my_app.testing = True
        self.app = my_app.test_client()
        self.path = '/api/v1.0/users/access'
        self.register_path = '/api/v1.0/users/register'
        self.users_path = 'api/v1.0/users/677'

        self.valid_user = {
            "email": "evil.cow@mammals.milk",
            "password": "dairycows",
            "name": "Evil Cow"
        }
        self.invalid_email = {
            "email": "evil.cow@milk",
            "password": "dairycows",
            "name": "Evil Cow"
        }
        self.invalid_password = {
            "email": "evil.cow@mammals.milk",
            "password": "cows",
            "name": "Evil Cow"
        }
        self.empty_name = {
            "email": "evil.cow@mammals.milk",
            "password": "dairycows",
            "name": ""
        }
        self.blank_email = {
            "email": "",
            "password": "dairycows",
            "name": "Evil Cow"
        }
        self.log_empty_email = {
            "email": "",
            "password": "dairycows"
        }
        self.log_empty_pass = {
            "email": "evil.cow@mammals.milk",
            "password": ""
        }

    def test_register_valid_user(self):
        res = self.app.post(self.register_path,
                            data=json.dumps(dict(
                                email="evil2.cow@mammals.milk",
                                password="dairycows",
                                name="Evil Cow")),
                            content_type='application/json',
                            follow_redirects=True

                            )
        response_unpack = json.loads(
            res.get_data().decode(sys.getdefaultencoding())
        )
        msg = "Fails to register new user"
        self.assertEqual(res.status_code, 201), msg
        self.assertIn('created', response_unpack,
                      msg=msg)

    def test_register_user_twice(self):
        res = self.app.post(self.register_path,
                            data=json.dumps(
                                self.valid_user),
                            content_type='application/json',
                            follow_redirects=True

                            )
        res = self.app.post(self.register_path,
                            data=json.dumps(
                                self.valid_user),
                            content_type='application/json',
                            follow_redirects=True

                            )
        what_we_expect = "It's bad manners to register twice"

        response_unpack = json.loads(
            res.get_data().decode(sys.getdefaultencoding())
        )

        self.assertEqual(409, res.status_code,
                         msg="Registers already registered user")

        self.assertTrue(response_unpack['message'] == what_we_expect,
                        msg="Registers already registered user")

    def test_register_invalid_email(self):
        res = self.app.post(self.register_path,
                            data=json.dumps(
                                self.invalid_email),
                            content_type='application/json',
                            follow_redirects=True

                            )
        response_unpack = json.loads(
            res.get_data().decode(sys.getdefaultencoding())
        )
        self.assertTrue(400, res.status_code
                        ), "Fails to request for valid email"
        self.assertEqual(response_unpack['message'], "Email format not invented yet.\
            Try something like evil.cow@mammals.milk")

    def test_register_short_password(self):
        res = self.app.post(self.register_path,
                            data=json.dumps(
                                self.invalid_password),
                            content_type='application/json',
                            follow_redirects=True

                            )
        response_unpack = json.loads(
            res.get_data().decode(sys.getdefaultencoding())
        )
        self.assertTrue(400, res.status_code
                        )
        self.assertIn("Password too short", response_unpack['message'],
                      msg="Failes to deny registeration using short password")

    def test_register_empty_name(self):
        res = self.app.post(self.register_path,
                            data=json.dumps(
                                self.empty_name),
                            content_type='application/json',
                            follow_redirects=True

                            )
        response_unpack = json.loads(
            res.get_data().decode(sys.getdefaultencoding())
        )
        self.assertTrue(400, res.status_code
                        )
        self.assertEqual("Please add a name",
                         response_unpack['message']['name'],
                         msg="Failes to deny registeration with empty name")

    def test_register_blank_email(self):
        res = self.app.post(self.register_path,
                            data=json.dumps(
                                self.blank_email),
                            content_type='application/json',
                            follow_redirects=True

                            )
        fail_msg = "You are not \
                            allowed here without email"
        response_unpack = json.loads(
            res.get_data().decode(sys.getdefaultencoding())
        )
        self.assertTrue(400, res.status_code
                        )
        self.assertEqual(fail_msg,
                         response_unpack['message']['email'],
                         msg="Failes to deny registeration using blank email")

    def test_login(self):
        res = self.app.post(self.register_path,
                            data=json.dumps(
                                self.valid_user),
                            content_type='application/json',
                            follow_redirects=True

                            )
        res = self.app.post(self.path,
                            data=json.dumps(
                                self.valid_user),
                            content_type='application/json',
                            follow_redirects=True

                            )
        response_unpack = json.loads(
            res.get_data().decode(sys.getdefaultencoding())
        )

        self.assertEqual(res.status_code, 200,
                         msg="Fails to login registered user")
        self.assertEqual(response_unpack['Status'], "Login successful")

    def test_login_unregistered_user(self):
        res = self.app.post(self.path,
                            data=json.dumps(dict(
                                email="lostcow.cow@mammals.milk",
                                password="dairycows",
                                name="Lost Cow")),
                            content_type='application/json',
                            follow_redirects=True

                            )
        response_unpack = json.loads(
            res.get_data().decode(sys.getdefaultencoding())
        )

        self.assertEqual(res.status_code, 401,
                         msg="Fails to login registered user")

        self.assertIn("Maybe register", response_unpack['message'])

    def test_login_wrong_password(self):
        res = self.app.post(self.register_path,
                            data=json.dumps(dict(
                                email="lostcow.cow@mammals.milk",
                                password="dairycows",
                                name="Lost Cow")),
                            content_type='application/json',
                            follow_redirects=True

                            )
        res = self.app.post(self.path,
                            data=json.dumps(dict(
                                email="lostcow.cow@mammals.milk",
                                password="wrongpass",
                                name="Lost Cow")),
                            content_type='application/json',
                            follow_redirects=True

                            )
        response_unpack = json.loads(
            res.get_data().decode(sys.getdefaultencoding())
        )

        self.assertEqual(res.status_code, 400,
                         msg="Fails.Logs in unregistered Password")
        print(response_unpack)

        self.assertEqual("Oops, that didn't work. Try again?",
                         response_unpack['message'])

    def test_user_nonexistent_record(self):
        res = self.app.get(self.users_path + '5643254',
                           follow_redirects=True
                           )
        self.assertEqual(res.status_code, 404)
