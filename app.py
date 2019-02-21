import argparse
from blacklist import BLACKLIST

from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

from database import db
from resources.item import Item
from resources.user import User, UserRegister, UserLogin, UserLogout
from resources.tokenRefresh import TokenRefresh

from models.userModel import UserModel

app = Flask(__name__)
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
app.secret_key = 'secret'
api = Api(app)

jwt = JWTManager(app)

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token['jti'] in BLACKLIST

@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    # get user type using identity(email)
    type_of_user = UserModel.get_user_type(identity)

    jwt_claim = {
        'is_admin': False,
        'is_contributor': False,
        'is_viewer': False
    }

    if type_of_user == 'admin':
        jwt_claim['is_admin'] = True
    elif type_of_user == 'viewer':
        jwt_claim['is_viewer'] = True
    elif type_of_user == 'contributor':
        jwt_claim['is_contributor'] = True

    return jwt_claim

api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(UserRegister, '/signup')
api.add_resource(User, '/user/<int:id>')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(TokenRefresh, '/refresh')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run the app.py blog app')
    parser.add_argument('--setup', dest='run_setup', action='store_true')

    args = parser.parse_args()
    if args.run_setup:
        db.dbSetup()
    else:
        app.run(debug=True)
