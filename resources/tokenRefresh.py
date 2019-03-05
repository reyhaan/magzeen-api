from flask_restful import Resource
from flask_jwt_extended import jwt_refresh_token_required, get_jwt_identity, create_access_token
from flask_api import status
from utils.reponseUtils import send_success

class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return send_success('Token created', {'access_token': new_token}, status.HTTP_200_OK)

class FreshToken(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=True)
        return send_success('Token created', {'access_token': new_token}, status.HTTP_200_OK)
