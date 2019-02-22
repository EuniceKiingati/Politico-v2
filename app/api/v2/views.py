from flask import Flask, jsonify, request, abort, make_response, render_template
import json
import datetime
import jwt
import os
from functools import wraps
from werkzeug.security import check_password_hash
from .utils.user_utils import UserValidation
from .utils.party_utils import PartyValidation
from .utils.office_utils import OfficeValidation
from .models.candidate_models import Candidate
from .models.vote_models import Vote
from .models.user_models import User
from .models.party_models import Party
from .models.office_models import Office


def bad_request(message):
    response = jsonify({
        "message": message,
        "status": 400,
    })
    response.status_code = 400
    return response


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

    def token_required(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            user1 = User()
            users = user1.get_all_User()
            current_user = None
            if 'token' in request.headers:
                token = request.headers['token']
                if not token:
                    return jsonify({
                        'message': 'token is missing',
                        'status': '401'
                    })
                # verify if token is valid
                try:
                    data = jwt.decode(token, app.config['SECRET_KEY'])
                    for user in users:
                        if user['username'] == data['username']:
                            current_user = user

                except:
                    return jsonify({
                        'message': 'token is invalid',
                        'status': 401
                    })

            return f(current_user, *args, **kwargs)
        return decorated

    @app.route('/', methods=['GET'])
    def home():
        return render_template('index.html')

    @app.route('/api/v2/users', methods=['POST'])
    def sign_up():
        data = request.get_json()

        validate = UserValidation(data)
        validate.validate_signup()
        new_user = User(data)
        new_user.save()

        userobj = User()
        userlist = userobj.get_all_User()
        for user in userlist:
            del user['password']
            if user['username'] == data['username']:
                response = jsonify({
                    "message": "user created successfully",
                    "status": 201,
                    "data": user
                })
                response.status_code = 201
                return response

    @app.route('/api/v2/users/login', methods=['POST'])
    def login():
        data = request.get_json()  # getting a json objectfrom request
        User_object = User()
        Userlist = User_object.get_all_User()

        username = data['username'].strip()
        password = data['password'].strip()

        for user in Userlist:

            if user['username'] == username and check_password_hash(user['password'], password):
                token = jwt.encode({'username': data['username'], 'exp': datetime.datetime.utcnow(
                ) + datetime.timedelta(hours=24)}, app.config['SECRET_KEY'])

                return make_response(

                    jsonify(
                        {
                            # decode to the regular string
                            'token': token.decode('UTF-8'),
                            'Message': "Successfully logged in"

                        }), 200)

        return make_response(jsonify({
            'Status': 'Failed',
            'Message': "No such user found. Check your login credentials"
        }), 404)

    @app.route('/api/v2/parties', methods=['POST'])
    @token_required
    def create_parties(current_user):

        data = request.get_json()
        # getting a json object from request
        if current_user and current_user['isadmin'] != True:
            return make_response(jsonify({
                'Status': 401,
                'Message': "You must be an admin"
            }), 401)
        if current_user and current_user['isadmin'] == True:
            validate = PartyValidation(data)
            validate.validate_create()
            new_party = Party(data)
            new_party.save_party()
            partyobj = Party()
            partylist = partyobj.get_all_parties()
            for party in partylist:
                if party['party_name'] == data['party_name']:
                    response = jsonify({
                        "message": "party created successfully",
                        "status": "201",
                        "data": party
                    })
            response.status_code = 201
            return response

    @app.route('/api/v2/parties', methods=['GET'])
    def get_parties():
        partyobj = Party()
        party = partyobj.get_all_parties()
        response = jsonify({
            "message": "Political parties retrieved successfully",
            "status": 200,
            "data": party
        })
        response.status_code = 200
        return response

    @app.route('/api/v2/parties/<int:party_id>', methods=['GET'])
    def single_political_party(party_id):
        single_party = Party()
        partylist = single_party.get_all_parties()

        for party in partylist:
            if party['party_id'] == party_id:
                response = jsonify({
                    "status": 200,
                    "data": party
                })
                response.status_code = 200
                return response
        response = jsonify({
            "message": "Party not found",
            "status": 404,
        })
        response.status_code = 404
        return response

    @app.route('/api/v2/parties/<int:party_id>', methods=['DELETE'])
    @token_required
    def delete_political_party(current_user, party_id):
        if current_user and current_user['isadmin'] != True:
            return make_response(jsonify({
                'Status': 'Failed',
                'Message': "You must be an admin"
            }), 401)
        if current_user and current_user['isadmin'] == True:
            single_party = Party()
            partylist = single_party.get_all_parties()
            for party in partylist:
                if party['party_id'] == party_id:
                    single_party.delete__party(party_id)

                    response = jsonify({
                        "message": "Political parties deleted successfully",
                        "status": 200,
                    })
                    response.status_code = 200
                    return response
            response = jsonify({
                "message": "Party not found",
                "status": 404,
            })
            response.status_code = 404
            return response

    @app.route('/api/v2/parties/<int:party_id>/name', methods=['PATCH'])
    @token_required
    def edit_party_name(current_user, party_id):
        single_party = Party()
        partylist = single_party.get_all_parties()

        data = request.get_json()  # data being passed
        if current_user and current_user['isadmin'] != True:
            return make_response(jsonify({
                'Status': 'Failed',
                'Message': "You must be an admin"
            }), 401)
        if current_user and current_user['isadmin'] == True:
            party_name = data['party_name']
            for party in partylist:
                if party_name == party["party_name"] and party['party_id'] != party_id:
                    message = "party name {} already taken".format(party_name)
                    return bad_request(message)
                if party['party_id'] == party_id:
                    single_party.update__party(party_id, party_name)
                    partylist = single_party.get_all_parties()
                    party = [
                        party for party in partylist if party['party_id'] == party_id]
                    response = jsonify({
                        "message": "Pollitical party updated successfully",
                        "status": 200,
                        "data": party
                    })
                    response.status_code = 200
                    return response
            response = jsonify({"message": "Party not found",
                                "status": 404
                                })
            response.status_code = 404
            return response

    @app.route('/api/v2/offices', methods=['POST'])
    @token_required
    def create_offices(current_user):
        data = request.get_json()  # getting a json object from request
        if current_user and current_user['isadmin'] != True:
            return make_response(jsonify({
                'Status': 'Failed',
                'Message': "You must be an admin"
            }), 401)
        if current_user and current_user['isadmin'] == True:
            validate = OfficeValidation(data)
            validate.validate_create()
            new_office = Office(data)
            new_office.save_office()
            officeobj = Office()
            officelist = officeobj.get_all_offices()
            for office in officelist:
                if office['office_name'] == data['office_name']:
                    response = jsonify({
                        "message": "office created successfully",
                        "status": "201",
                        "data": office
                    })
            response.status_code = 201
            return response

    @app.route('/api/v2/offices', methods=['GET'])
    def get_offices():
        officeobj = Office()
        office = officeobj.get_all_offices()
        response = jsonify({
            "message": "Political offices retrieved successfully",
            "status": 200,
            "data": office
        })
        response.status_code = 200
        return response

    @app.route('/api/v2/office/<int:office_id>', methods=['GET'])
    def single_political_office(office_id):
        single_office = Office()
        officelist = single_office.get_all_offices()

        for office in officelist:
            if office['office_id'] == office_id:
                response = jsonify({
                    "status": 200,
                    "data": office
                })
                response.status_code = 200
                return response
        response = jsonify({
            "message": "office not found",
            "status": 404,
        })
        response.status_code = 404
        return response

    @app.route('/api/v2/office/<int:office_id>/register', methods=['POST'])
    def create_candidate(office_id):
        data = request.get_json()
        try:
            user_id = data['user_id']
        except Exception:
            response = jsonify({
                "message": "User ID is missing",
                "status": 400,
            })
            response.status_code = 400
            return response
        officeobj = Office()
        officelist = officeobj.get_all_offices()
        User_object = User()
        Userlist = User_object.get_all_User()
        candidateobj = Candidate()
        candidatelist = candidateobj.get_all_candidates()
        for office in officelist:
            if office['office_id'] == office_id:
                for user in Userlist:

                    if user['user_id'] == user_id:
                        candidate = [
                            candidate for candidate in candidatelist if candidate['user_id'] == user_id]
                        if candidate:
                            response = jsonify({
                                "message": "Candidate already exists",
                                "status": 403,
                            })
                            response.status_code = 403
                            return response
                        new_candidate_data = {
                            "user_id": user_id,
                            "office_id": office_id
                        }
                        new_candidate = Candidate(new_candidate_data)
                        new_candidate.save()
                        candidatelist = candidateobj.get_all_candidates()
                        for candidate in candidatelist:
                            if candidate['user_id'] == new_candidate_data['user_id']:
                                response = jsonify({
                                    "message": "Candidate created successfully",
                                    "status": 201,
                                    "data": candidate
                                })
                                response.status_code = 201
                                return response
                response = jsonify({
                    "message": "User not found",
                    "status": 404,
                })
                response.status_code = 404
                return response
        response = jsonify({
            "message": "Office not found",
            "status": 404,
        })
        response.status_code = 404
        return response

    @app.route('/api/v2/votes', methods=['POST'])
    def vote():
        data = request.get_json()
        User_object = User()
        Userlist = User_object.get_all_User()
        officeobj = Office()
        officelist = officeobj.get_all_offices()
        candidateobj = Candidate()
        candidatelist = candidateobj.get_all_candidates()
        for user in Userlist:
            if user['voter_id'] == data['voter_id']:
                for office in officelist:
                    if office['office_id'] == data['office_id']:
                        for candidate in candidatelist:
                            if candidate['candidate_id'] == data['candidate_id']:
                                new_vote = Vote(data)
                                new_vote.save_vote()
                                response = jsonify({
                                    "message": "voted successfully",
                                    "status": 201,
                                    "data": candidate
                                })
                                response.status_code = 201
                                return response
                response = jsonify({
                    "message": "office not found",
                    "status": 404,
                })
                response.status_code = 404
                return response

        response = jsonify({
            "message": "User not found",
            "status": 404,
        })
        response.status_code = 404
        return response

    @app.route('/api/v2/office/<int:office_id>/result', methods=['GET'])
    def results(office_id):
        office_obj = Office()
        office_list = office_obj.get_all_offices()
        vote_obj = Vote()
        votes = vote_obj.get_all_votes()
        for office in office_list:
            if office['office_id'] == office_id:
                response = jsonify({
                    "message": "office data",
                    "status": 200,
                    "data": votes
                })
                response.status_code = 200
                return response
        response = jsonify({
            "message": "office not found",
            "status": 404,
        })
        response.status_code = 404
        return response
    return app
