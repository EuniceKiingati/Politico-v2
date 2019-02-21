from .base_test import *


class TestUser(BaseTest):
    '''Define a class for the tests'''

    def test_admin__signup(self):
        '''Admin can sign up sucessfully'''
        response = self.signup_admin
        self.assertEqual(response.status_code, 201)

    def test_admin__login(self):

        response = self.login_admin
        self.assertEqual(response.status_code, 200)

    def test_normal_user_signup(self):
        '''Admin can sign up sucessfully'''
        response = self.signup_normal_user
        self.assertEqual(response.status_code, 201)

    def test_normal_user_login(self):

        response = self.login_normal_user
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
        self.assertIn(b"Username is missing", response.data)

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
        #self.assertIn(b"Password is missing", response.data)

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
        self.assertEqual(response.status_code, 400)

    def test_missing_id(self):
        user = json.dumps({
            "username": "yunweis2",
            "voter_id": "",
            "password": "Yunis6tg@#",
            "email": "yuneris500@gmail.com",
            "isadmin": "True"})
        response = self.test_client.post(
            '/api/v2/users', data=user,
            headers={
                'content-type': 'application/json'})
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"voter_id is missing", response.data)

    def test_username_not_string(self):
        user = json.dumps({
            "username": 340,
            "voter_id": "voe25096",
            "password": "Yunis6tg@#",
            "email": "yunis500@gmail.com",
            "isadmin": "True"})
        response = self.test_client.post(
            '/api/v2/users', data=user,
            headers={
                'content-type': 'application/json'})
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Username must be a string", response.data)

    def test_password_not_string(self):
        user = json.dumps({
            "username": "340",
            "voter_id": "votee256",
            "password": 809,
            "email": "yunis500@gmail.com",
            "isadmin": "True"})
        response = self.test_client.post(
            '/api/v2/users', data=user,
            headers={
                'content-type': 'application/json'})
        self.assertIn(b"Password must be a string", response.data)
        self.assertEqual(response.status_code, 400)

    def test_password_no_uppercase(self):
        user = json.dumps({
            "username": "340",
            "voter_id": "vote256",
            "password": "yunistg@#",
            "email": "yunis500@gmail.com",
            "isadmin": "True"})
        response = self.test_client.post(
            '/api/v2/users', data=user,
            headers={
                'content-type': 'application/json'})
        self.assertEqual(response.status_code, 400)

    def test_password_no_lowercase(self):
        user = json.dumps({
            "username": "340",
            "voter_id": "vote256",
            "password": "YUNISTG@#",
            "email": "yunis500@gmail.com",
            "isadmin": "True"})
        response = self.test_client.post(
            '/api/v2/users', data=user,
            headers={
                'content-type': 'application/json'})
        self.assertEqual(response.status_code, 400)

    def test_password_no_special_ch(self):
        user = json.dumps({
            "username": "yunis",
            "voter_id": "vote256",
            "password": "Yunis6tg",
            "email": "yunis500@gmail.com",
            "isadmin": "True"})
        response = self.test_client.post(
            '/api/v2/users', data=user,
            headers={
                'content-type': 'application/json'})
        self.assertEqual(response.status_code, 400)

    def test_password_more_than_12_ch(self):
        user = json.dumps({
            "username": "yunis",
            "voter_id": "vote256",
            "password": "Yunis6tg#@$%^&*dfjd",
            "email": "yunis500@gmail.com",
            "isadmin": "True"})
        response = self.test_client.post(
            '/api/v2/users', data=user,
            headers={
                'content-type': 'application/json'})
        self.assertEqual(response.status_code, 400)

    def test_password_less_than_6_ch(self):
        user = json.dumps({
            "username": "yunis",
            "voter_id": "vote256",
            "password": "Yg#",
            "email": "yunis500@gmail.com",
            "isadmin": "True"})
        response = self.test_client.post(
            '/api/v2/users', data=user,
            headers={
                'content-type': 'application/json'})
        self.assertEqual(response.status_code, 400)

    def test_invalid_email(self):
        user = json.dumps({
            "username": "yunis",
            "voter_id": "vote256",
            "password": "Yg#",
            "email": "yunis500.com",
            "isadmin": "True"})
        response = self.test_client.post(
            '/api/v2/users', data=user,
            headers={
                'content-type': 'application/json'})
        self.assertEqual(response.status_code, 400)

    def test_missing_email(self):
        user = json.dumps({
            "username": "yunis",
            "voter_id": "vote256",
            "password": "Yunis6tg@#",
            "email": "",
            "isadmin": True})
        response = self.test_client.post(
            '/api/v2/users', data=user,
            headers={
                'content-type': 'application/json'})
        self.assertEqual(response.status_code, 400)

    def test_create_candidate(self):
        
        response = self.create_candidate
        self.assertEqual(response.status_code, 201)

    def test_candidate_already_exists(self):
        candidate = json.dumps({
            "user_id": 1})
        response = self.test_client.post(
            '/api/v2/office/1/register', data=candidate,
            headers={
                'content-type': 'application/json',
                'token': self.admin_token['token']})
        self.assertEqual(response.status_code, 403)
