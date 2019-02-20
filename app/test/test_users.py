from .base_test import *


class TestUser(BaseTest):
    '''Define a class for the tests'''

    def test_admin__signup(self):
        '''Admin can sign up sucessfully'''
        response = self.signup_admin
        self.assertEqual(response.status_code, 201)

    def test_admin__login(self):

        response = self.login_admin
        print(response.data)
        self.assertEqual(response.status_code, 200)

    def test_normal_user_signup(self):
        '''Admin can sign up sucessfully'''
        response = self.signup_normal_user
        print(response.data)
        self.assertEqual(response.status_code, 201)

    def test_normal_user_login(self):

        response = self.login_normal_user
        print(response.data)
        self.assertEqual(response.status_code, 200)

    def test_missing_username(self):
        user = json.dumps({
            "username": "",
            "voter_id": "vote256",
            "password": "Yunis6tg@#",
            "email": "yunis500@gmail.com",
            "isadmin": True})
        response = self.test_client.post(
            '/api/v2/users', data=user,
            headers={
                'content-type': 'application/json'})
        self.assertEqual(response.status_code, 400)

    def test_missing_password(self):
        user = json.dumps({
            "username": "yunis",
            "voter_id": "vote256",
            "password": "",
            "email": "yunis500@gmail.com",
            "isadmin": True})
        response = self.test_client.post(
            '/api/v2/users', data=user,
            headers={
                'content-type': 'application/json'})
        self.assertEqual(response.status_code, 400)

    def test_existing_username(self):
        user = json.dumps({

            "username": "yunis",
            "voter_id": "vote256",
            "password": "Yunis6tg@#",
            "email": "yunis500@gmail.com",
            "isadmin": True
        })
        response = self.test_client.post(
            '/api/v2/users', data=user,
            headers={'content-type': 'application/json'})
        print(response.data)
        self.assertEqual(response.status_code, 400)
