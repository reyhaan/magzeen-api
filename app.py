from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from flask_jwt import JWT, jwt_required
from security import authenticate, identity

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
    @jwt_required()
    def get(self, name):
        item = next(filter(lambda x: x['name'] == name, items), None)
        return {'item': item}, 200 if item else 404
    
    def post(self, name):
        data = request.get_json()
        item = {'name': data['name'], 'data': data['desc']}
        items.append(item)
        return item, 201

api.add_resource(Item, '/item/<string:name>')

if __name__ == '__main__':
    app.run(debug=True)