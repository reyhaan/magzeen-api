import json
from flask import request, jsonify, make_response
from flask_restful import Resource, reqparse
from flask_api import status
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_claims, get_raw_jwt
from models.userModel import UserModel
from utils.reponseUtils import send_error, send_success, DateTimeEncoder
from blacklist import BLACKLIST

class UserLogin(Resource):

    parser = reqparse.RequestParser()

    parser.add_argument(
        'email',
        type=str,
        required=True,
        help='email cannot be left blank!'
    )

    parser.add_argument(
        'password',
        type=str,
        required=True,
        help='password cannot be left blank!'
    )

    def post(self):
        data = UserLogin.parser.parse_args()
        email = data['email']
        password = data['password']
        user_object = UserModel(email, password)
        user = user_object.check_if_user_exists_by_email(email)
        if user == 0:
            return send_error('user does not exist', status.HTTP_400_BAD_REQUEST)
        else:
            user = user_object.verify_user(email, password)

            if user == 0:
                return send_error('either email/password is not correct', status.HTTP_401_UNAUTHORIZED)
            else:
                access_token = create_access_token(identity=email, fresh=True)
                refresh_token = create_refresh_token(identity=email)
                return send_success(
                    'success',
                    {
                        'access_token': access_token,
                        'refresh_token': refresh_token,
                        'user': user
                    },
                    status.HTTP_200_OK
                )

class UserLogout(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        BLACKLIST.append(jti)
        return send_success('Success', {'message': 'successfully logged out.'}, status.HTTP_200_OK)

class UserRegister(Resource):

    parser = reqparse.RequestParser()

    parser.add_argument(
        'email',
        type=str,
        required=True,
        help='email cannot be left blank!'
    )

    parser.add_argument(
        'password',
        type=str,
        required=True,
        help='password cannot be left blank!'
    )

    def post(self):
        data = UserRegister.parser.parse_args()
        email = data['email']
        password = data['password']
        user_object = UserModel(email, password)
        # check if user already exixsts
        new_user = user_object.check_if_user_exists(email)
        if new_user == 0:
            new_user = user_object.add_user(email, password)
            return send_success('user created', new_user, status.HTTP_201_CREATED)
        else:
            return send_error('user already exists', status.HTTP_409_CONFLICT)

class User(Resource):

    user_object = UserModel()

    @jwt_required
    def get(self, id):
        # handle claims
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return send_error('Admin privileges required', status.HTTP_401_UNAUTHORIZED)
        user_exists = User.user_object.check_if_user_exists_by_id(id)
        if not user_exists:
            return send_error('user does not exist', status.HTTP_404_NOT_FOUND)
        else:
            user = User.user_object.find_user_by_id(id)
            if user:
                return send_success('success', user, status.HTTP_200_OK)

    @jwt_required
    def delete(self, id):
        user_exists = User.user_object.check_if_user_exists_by_id(id)
        if not user_exists:
            return send_error('user does not exist', status.HTTP_400_BAD_REQUEST)

        is_deleted = User.user_object.delete_user(id)

        if is_deleted:
            return send_success('success', None, status.HTTP_200_OK)
        else:
            return send_error('something went wrong', status.HTTP_400_BAD_REQUEST)

    @jwt_required
    def put(self, id):
        # check if user already exixsts
        new_user = User.user_object.check_if_user_exists_by_id(id)
        if new_user == 0:
            return send_error('user does not exist', status.HTTP_409_CONFLICT)
        else:
            data = json.loads(request.data)
            new_user = User.user_object.update_user(data, id)
            return send_success('success', new_user, status.HTTP_200_OK)
