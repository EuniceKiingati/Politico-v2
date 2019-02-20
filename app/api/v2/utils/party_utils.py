import re
from flask import jsonify, abort
from app.api.v2.models import Party


def bad_request(message):
    response = jsonify({
        "error": message,
        "status": 400,
    })
    response.status_code = 400
    abort(response)


class PartyValidation():
    def __init__(self, data):
        self.data=data
        self.party_name = data['party_name']
        self.hqaddress = data['hqaddress']
        self.logoUrl = data['logoUrl']

    def validate_create(self):
        partylist=Party.get_all_parties(self)

        if not self.data:
            message = "You must provide create_party data"
            return bad_request(message)
        if self.party_name == "":
            message = "party_name is missing"
            return bad_request(message)
        for party in partylist:
            if self.party_name == party["party_name"]:
                message = "party_name {} already taken".format(self.party_name)
                return bad_request(message)
        if type(self.party_name) != str:
            message = "party name must be a string"
            return bad_request(message)
        return True