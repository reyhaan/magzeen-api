import argparse
from flask import Flask, jsonify, request
from flask_restful import Api, Resource, reqparse
from flask_jwt import JWT, jwt_required
from security import authenticate, identity
from models import db

app = Flask(__name__)
app.secret_key = 'secret'
api = Api(app)

jwt = JWT(app ,authenticate, identity)

items = [
    {'name': '1', 'data': 'keyboard'},
    {'name': '2', 'data': 'mouse'},
    {'name': '3', 'data': 'laptop'}
]

class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help='This field cannot be left blank!'
    )

    @jwt_required()
    def get(self, name):
        item = next(filter(lambda x: x['name'] == name, items), None)
        return {'item': item}, 200 if item else 404
    
    def post(self, name):
        data = request.get_json()
        item = {'name': data['name'], 'data': data['desc']}
        items.append(item)
        return item, 201

    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message': 'item deleted!'}

    def put(self, name):
        data = Item.parser.parse_args()
        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            item = {'name': name, data: data['desc']}
            items.append(item)
        else:
            item.update(data)
        return item

api.add_resource(Item, '/item/<string:name>')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run the app.py blog app')
    parser.add_argument('--setup', dest='run_setup', action='store_true')

    args = parser.parse_args()
    if args.run_setup:
        db.dbSetup()
    else:
        app.run(debug=True)
