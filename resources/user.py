from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models import userModel

items = [
    {'name': '1', 'data': 'keyboard'},
    {'name': '2', 'data': 'mouse'},
    {'name': '3', 'data': 'laptop'}
]


class UserRegister(Resource):

    parser = reqparse.RequestParser()

    parser.add_argument(
        'username',
        type=str,
        required=True,
        help='username cannot be left blank!'
    )

    parser.add_argument(
        'password',
        type=str,
        required=True,
        help='password cannot be left blank!'
    )

    def post(self):
        data = UserRegister.parser.parse_args()
        username = data['username']
        password = data['password']
        user = userModel.addUser(username, password)
        return user, 201


class User(Resource):

    @jwt_required()
    def get(self, name):
        item = next(filter(lambda x: x['name'] == name, items), None)
        return {'item': item}, 200 if item else 404

    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message': 'item deleted!'}

    def put(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument(
            'price',
            type=float,
            required=True,
            help='This field cannot be left blank!'
        )
        data = parser.parse_args()
        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            item = {'name': name, data: data['desc']}
            items.append(item)
        else:
            item.update(data)
        return item