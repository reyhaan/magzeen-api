import json
from flask import request, jsonify
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.userModel import UserModel

items = [
    {'name': '1', 'data': 'keyboard'},
    {'name': '2', 'data': 'mouse'},
    {'name': '3', 'data': 'laptop'}
]


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
            return new_user, 201
        else:
            return 'user already exists', 409

class User(Resource):

    parser = reqparse.RequestParser()

    @jwt_required()
    def get(self, name):
        item = next(filter(lambda x: x['name'] == name, items), None)
        return {'item': item}, 200 if item else 404

    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message': 'item deleted!'}

    def put(self, id):
        # check if user already exixsts
        user_object = UserModel()
        user = user_object.find_user_by_id(id)
        new_user = user_object.check_if_user_exists_by_email(user['email'])
        if new_user == 0:
            return 'user does not exist', 409
        else:
            data = json.loads(request.data)
            new_user = user_object.update_user(data, user['user_id'])
            return new_user, 200
