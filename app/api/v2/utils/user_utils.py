import re
from flask import jsonify, abort
from app.api.v2.models import User
from email_validator import validate_email, EmailNotValidError



def bad_request(message):
    response = jsonify({
        "error": message,
        "status": 400,
    })
    response.status_code = 400
    abort(response)


class UserValidation(User):
    def __init__(self, data):
        self.data=data
        self.username = data['username']
        self.voter_id=data['voter_id']
        self.email = data['email']
        self.password = data['password']
        self.isadmin = data['role']

    def validate_signup(self):
        Userlist=User.get_all_User(self)

        if not self.data:
            message = "You must provide signup data"
            return bad_request(message)
        try:
            v = validate_email(self.email) # validate and get info
            email = v["email"] # replace with normalized form
        except EmailNotValidError as e:
            # email is not valid, exception message is human-readable
            print(str(e))
        if self.username == "":
            message = 'Username is missing'
            return bad_request(message)
        for user in Userlist:
            if self.username == user["username"]:
                message = "username {} already taken".format(self.username)
                return bad_request(message)
            if self.voter_id==user["voter_id"]:
                message= "voter_id {} already taken".format(self.voter_id)
                return bad_request(message)
        if type(self.username) != str:
            message = "Username must be a string"
            return bad_request(message)
        if self.voter_id=="":
            message="voter_id is missing"
            return bad_request(message)
        if len(self.voter_id) <= 6 or len(self.voter_id) > 10:
            message = "Voter_id must be at least 6 and at most 10 ch long"
            return bad_request(message)

        if self.password == "":
            message = "Password is missing"
            return bad_request(message)
        if type(self.password) != str:
            message = "Password must be a string"
            return bad_request(message)
        if len(self.password) <= 6 or len(self.password) > 12:
            message = "Password must be at least 6 and at most 10 ch long"
            return bad_request(message)
        elif not any(char.isdigit() for char in self.password):
            message = "Password must have a digit"
            return bad_request(message)
        elif not any(char.isupper() for char in self.password):
            message = "Password must have an upper case character"
            return bad_request(message)
        elif not any(char.islower() for char in self.password):
            message = "Password must have a lower case character"
            return bad_request(message)
        elif not re.search("[#@$]", self.password):
            message = "Password must have one of the special charater [#@$]"
            return bad_request(message)
        return True

    def validate_login(self, data):
        self.user_obj = User.get_all_User(self)
        if not self.data:

            message = "You must provide login data"
            return bad_request(message)

        # gets the value that the key represents
        username = data['username']
        if username == "":
            message = 'Username is missing'
            return bad_request(message)
        password = data['password']
        if password == "":
            message = "Password is missing"
            return bad_request(message)
        for user in data:
            if user['username'] == username and user['password'] == password:  
                response = jsonify({
                    "message": "User login successful",
                    "status": 200,
                    "data": user
                })
                response.status_code = 200
                return response
        response = jsonify({
            "message": "User login failed, Check your credentials",
            "status": 401, 
        })
        response.status_code = 401
        return response