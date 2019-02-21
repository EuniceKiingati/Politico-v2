from.base_test import *


class TestParties(BaseTest):
    def test_normal_user_create_party(self):
        party = json.dumps({

            "party_name": "Party2",
            "hqaddress": "sampleaddress",
            "logoUrl": "sampleurl"
        })
        response = self.test_client.post(
            '/api/v2/parties',
            data=party,
            headers={
                'content-type': 'application/json',
                'token': self.normal_user_token['token']})
        self.assertEqual(response.status_code, 401)

    def test_admin_create_party(self):
        response = self.create_party
        self.assertEqual(response.status_code, 201)

    def test_missing_party_name(self):
        party = json.dumps({
            "party_name": "",
            "hqaddress": "sampleaddress",
            "logoUrl": "sampleurl"})
        response = self.test_client.post(
            '/api/v2/parties', data=party,
            headers={
                'token': self.admin_token['token'],
                'content-type': 'application/json'})
        print(response.data)
        self.assertEqual(response.status_code, 400)

    def test_existing_party_name(self):
        party = json.dumps({

            "party_name": "Party1",
            "hqaddress": "sampleaddress",
            "logoUrl": "sampleurl"
        })
        response = self.test_client.post(
            '/api/v2/parties', data=party,
            headers={
                'token': self.admin_token['token'],

                'content-type': 'application/json'})
        self.assertEqual(response.status_code, 400)

    def test_get_single_party(self):
        response = self.test_client.get(
            '/api/v2/parties/1',
            headers={
                'token': self.normal_user_token['token']
            })
        self.assertEqual(response.status_code, 200)

    def test_delete_party(self):
        response = self.test_client.delete(
            '/api/v2/parties/{}'.format(1), headers={
                'token': self.admin_token['token']})
        self.assertEqual(response.status_code, 200)

    def test_get_all_parties(self):
        response = self.test_client.get(
            '/api/v2/parties', headers={
                'token': self.normal_user_token['token']})
        self.assertEqual(response.status_code, 200)

    def test_party_name_not_string(self):
        data = json.dumps({
            "party_name": 254,
            "hqaddress": "sampleaddress",
            "logoUrl": "sampleUrl"})
        response = self.test_client.post(
            '/api/v2/parties',
            headers={
                'content-type': 'application/json',
                'token': self.admin_token['token']})
        self.assertEqual(response.status_code, 400)
