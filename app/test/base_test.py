import unittest
import json
from app.api.v2.models.database_connection import Dbase
from app.api.v2.views import create_app


class BaseTest(unittest.TestCase):
    '''defining setup and teardown methods'''

    def setUp(self):
        # Create a database object
        self.db_object = Dbase()
        self.db_object.destroy_tables()
        self.db_object.create_tables()

        self.app = create_app()
        self.test_client = self.app.test_client()
        # details for admin signup
        self.admin_signup_data = json.dumps({
            "username": "yunis",
            "voter_id": "vot5256",
            "password": "Yunis6tg@#",
            "email": "yunis500@gmail.com",
            "isadmin": True
        })
        # details for admin login
        self.admin_login_data = json.dumps({
            "username": "yunis",
            "password": "Yunis6tg@#",
        })
        # normal user signup
        self.normal_user_signup_data = json.dumps({
            "username": "yunis1",
            "voter_id": "vote257",
            "email": "yunis1@gmail.com",
            "password": "Yunis5600@",
            "isadmin": False
        })
        self.normal_user_login_data = json.dumps({
            "username": "yunis1",
            "password": "Yunis5600@"
        })
        # party details
        self.party = json.dumps({
            "party_name": "Party1",
            "hqaddress": "sampleaddress",
            "logoUrl": "sampleurl"
        })
        self.office = json.dumps({
            "office_name": "Governor",
            "office_type": "sampletype",

        })
        self.vote_data = json.dumps({
            "voter_id": "vot5256",
            "office_id": 1,
            "candidate_id": 1


        })
        self.candidate_data = json.dumps({
            "user_id": 1})

        self.signup_admin = self.test_client.post(
            "/api/v2/users",
            data=self.admin_signup_data,
            headers={
                'content-type': 'application/json'
            })
        self.login_admin = self.test_client.post(
            "/api/v2/users/login",
            data=self.admin_login_data,
            content_type='application/json')
        self.admin_token = json.loads(self.login_admin.data.decode())
        self.signup_normal_user = self.test_client.post(
            "/api/v2/users",
            data=self.normal_user_signup_data,
            content_type='application/json')

        self.login_normal_user = self.test_client.post(
            "/api/v2/users/login",
            data=self.normal_user_login_data,
            content_type='application/json')
        self.normal_user_token = json.loads(
            self.login_normal_user.data.decode())

        self.create_party = self.test_client.post(
            '/api/v2/parties',
            data=self.party,
            headers={
                'token': self.admin_token['token'],
                'content-type': 'application/json'
            })
        self.create_office = self.test_client.post(
            '/api/v2/offices',
            data=self.office,
            headers={
                'token': self.admin_token['token'],
                'content-type': 'application/json'
            })
        self.create_candidate = self.test_client.post(
            '/api/v2/office/1/register', data=self.candidate_data,
            headers={
                'content-type': 'application/json',
                'token': self.admin_token['token']})
        self.vote = self.test_client.post(
            '/api/v2/votes', data=self.vote_data,
            headers={
                'content-type': 'application/json',
                'token': self.admin_token['token']})
