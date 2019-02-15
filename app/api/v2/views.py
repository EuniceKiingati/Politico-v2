from flask import Flask, jsonify, request, abort,make_response, render_template
import json

from .utils.user_utils import UserValidation

from .models import Dbase
from .models import User,Party

def bad_request(message):
    response = jsonify({
        "message": message,
        "status": 400,
    })
    response.status_code = 400
    return response


def create_app():
    app = Flask(__name__)

    @app.route('/', methods=['GET'])
    def home():
        return render_template('index.html')

    @app.route('/api/v2/User', methods=['POST'])
    def sign_up():
        data = request.get_json()
        dtb_obj= User(data)
        dtb_obj.save()

        validate = UserValidation(data)
        validate.validate_signup()
        new_user =User(data)
        new_user.save()

        response = jsonify({
            "message": "user created successfully",
            "status": 201,
            "data":"User"
        })
        response.status_code = 201
        return response


    @app.route('/api/v2/User/login', methods=['POST'])
    def login():
        data = request.get_json()  # getting a json objectfrom request
        User_object=User()
        Userlist=User_object.get_all_User()
        
        username = data['username'].strip()
        password = data['password'].strip()
        
        for user in Userlist:
            
            if user ['username'] == username and\
            user['password']==password:
                return make_response(

                    jsonify(
                        {'Message': "Successfully logged in"
                         
                         }), 200)
                

        return make_response(jsonify({
            'Status': 'Failed',
            'Message': "No such user found. Check your login credentials"
        }), 404)

    @app.route('/api/v2/parties', methods=['POST'])
    def create_parties():
        data = request.get_json()  # getting a json object from request
        # validate = ValidateParty(data)
        # validate.validate_create()
        new_party = Party(data)
        new_party.save_party()
        response = jsonify({
            "message": "party created successfully",
            "status": "201",
            "data":"Party"
        })
        response.status_code = 201
        return response
    
    @app.route('/api/v1/parties', methods=['GET'])
    def get_parties():
        response = jsonify({
            "message": "Political parties retrieved successfully",
            "status": 200,
            "data":"Party"
        })
        response.status_code = 200
        return response

    return app