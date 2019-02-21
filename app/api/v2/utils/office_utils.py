import re
from flask import jsonify, abort
from app.api.v2.models import Office


def bad_request(message):
    response = jsonify({
        "error": message,
        "status": 400,
    })
    response.status_code = 400
    abort(response)


class OfficeValidation():
    def __init__(self, data):
        self.data = data
        self.office_name = data['office_name']
        self.office_type = data['office_type']

    def validate_create(self):
        officelist = Office.get_all_offices(self)

        if not self.data:
            message = "You must provide create_office data"
            return bad_request(message)
        if self.office_name == "":
            message = "office_name is missing"
            return bad_request(message)
        for office in officelist:
            if self.office_name == office["office_name"]:
                message = "office_name {} already taken".format(
                    self.office_name)
                return bad_request(message)
        if type(self.office_name) != str:
            message = "office name must be a string"
            return bad_request(message)
        return True
