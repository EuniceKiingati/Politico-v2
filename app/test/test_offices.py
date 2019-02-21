from.base_test import *


class Testoffices(BaseTest):
    def test_normal_user_create_party(self):
        office = json.dumps({

            "office_name": "senator",
            "office_type": "sampletyypee",

        })
        response = self.test_client.post(
            '/api/v2/offices',
            data=office,
            headers={
                'content-type': 'application/json',
                'token': self.normal_user_token['token']})
        self.assertEqual(response.status_code, 401)

    def test_admin_create_office(self):
        response = self.create_office
        self.assertEqual(response.status_code, 201)

    def test_missing_office_name(self):
        office = json.dumps({
            "office_name": "",
            "office_type": "sampletyypee"})
        response = self.test_client.post(
            '/api/v2/offices', data=office,
            headers={
                'token': self.admin_token['token'],
                'content-type': 'application/json'})
        self.assertEqual(response.status_code, 400)

    def test_existing_office_name(self):
        office = json.dumps({

            "office_name": "Governor",
            "office_type": "sampletyypee"
        })
        response = self.test_client.post(
            '/api/v2/offices', data=office,
            headers={
                'token': self.admin_token['token'],

                'content-type': 'application/json'})
        self.assertEqual(response.status_code, 400)
