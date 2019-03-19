from functools import wraps
from flask_jwt_extended import get_raw_jwt
from flask_api import status
from models.userModel import UserModel
from utils.reponseUtils import send_error, send_success

def roles_accepted(roles=None):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            identity = get_raw_jwt()['identity']
            user_type = UserModel.get_user_type(identity)

            if user_type in roles:
                print("ALLOWED!")
            else:
                print("OOPS! UNAUTHORIZED ACCESS!")
                return send_error('Unauthorized', status.HTTP_401_UNAUTHORIZED)

            return f(*args, **kwargs)
        return decorated_function
    return decorator
