import json
import datetime
from flask_api import status
from flask import make_response, jsonify

def send_error(msg, code):
    return make_response(jsonify(message=msg, code=code, error=True, success=False), code)

def send_success(msg, data, code):
    return make_response(jsonify(message=msg, data=data, code=code, error=False, success=True), code)

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            encoded_object = list(obj.timetuple())[0:6]
        else:
            encoded_object = json.JSONEncoder.default(self, obj)
        return encoded_object
