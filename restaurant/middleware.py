from rest_framework.response import Response
from rest_framework_jwt.authentication import api_settings
from rest_framework import status
import jwt
from django.http import HttpResponse
import json


def check_token(token):
    try:
        decoded = jwt.decode(token, 'secret', algorithms=['HS256'])
        if decoded:
            return decoded.get('id')
        else:
            return False
    except:
        return False


class Generate:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not (request.path.startswith("/user/signup/") or request.path.startswith("/user/signin/")):
            token = request.headers.get('token')
            if not token:
                return HttpResponse(json.dumps({"Message": "Please fill the empty field"}), status.HTTP_400_BAD_REQUEST)
            else:
                if not check_token(token):
                    return HttpResponse(json.dumps({"message": "Invalid Token"}), status.HTTP_401_UNAUTHORIZED)

                else:
                    # user = check_token(token)
                    request.user_id = check_token(token)
        res = self.get_response(request)
        return res