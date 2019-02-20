import unittest
import json
from app.api.v2.models import *
from app.api.v2.views import create_app


class BaseTest(unittest.TestCase):
    '''defining setup and teardown methods'''
    def setUp(self):
        # Create a database object
        self.db_object = Dbase()
        self.db_object.destroy_tables()
        self.db_object.create_tables()

        self.app=create_app()
        self.test_client= self.app.test_client()
        #details for admin signup
        self.admin_signup_data=json.dumps({
            "username": "yunis",
            "voter_id":"vote256",
            "password": "Yunis6tg@#",
            "email": "yunis500@gmail.com",
            "isadmin":True
        })
        #details for admin login
        self.admin_login=json.dumps({
           "username": "yunis",
           "password": "Yunis6tg@#", 
        })
        #normal user signup
        self.normal_user_info = json.dumps({
            "username": "yunis",
            "email": "yunis@gmail.com",
            "password": "Yunis5600@",
            "isadmin":False
        })
        self.normal_user_login_info = json.dumps({
            "username": "yunis",
            "password": "Yunis5600@"
            })
        
        self.signup_admin = self.test_client.post(
            "/api/v2/users",
            data=self.admin_signup_data,
            headers={
                'content-type': 'application/json'
            })
        self.login_admin = self.test_client.post(
            "/api/v2/users/login",
            data=self.admin_login,
            content_type='application/json')
        # self.admin_token = json.loads(self.login_admin.data.decode())