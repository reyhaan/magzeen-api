import argparse

from flask import Flask
from flask_jwt import JWT
from flask_restful import Api

from models import db
from resources.item import Item
from resources.user import User, UserRegister
from security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'secret'
api = Api(app)

jwt = JWT(app, authenticate, identity)

api.add_resource(Item, '/item/<string:name>')
api.add_resource(User, '/user/<string:name>')
api.add_resource(UserRegister, '/user/signup')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run the app.py blog app')
    parser.add_argument('--setup', dest='run_setup', action='store_true')

    args = parser.parse_args()
    if args.run_setup:
        db.dbSetup()
    else:
        app.run(debug=True)
