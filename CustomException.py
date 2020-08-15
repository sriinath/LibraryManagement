import json
from json.decoder import JSONDecodeError
from django.http import JsonResponse 

class CustomException(Exception):
    def __init__(self, status_code, message, info=dict()):
        self.status_code = status_code
        self.message = message
        self.info = info

    def __str__(self):
        return self.message

def exception_handler(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except CustomException as exc:
            return JsonResponse(dict(
                message=exc.message,
                **exc.info
            ), status=exc.status_code)
        except JSONDecodeError as exc:
            print(exc)
            return JsonResponse({
                'status': 'Failure',
                'message': 'JSON provided in request body is not valid'
            }, status=400)
        except AssertionError as exc:
            print(exc)
            message = str(exc)
            if not message:
                message = 'Please make sure the request is valid'
            return JsonResponse({
                'status': 'Failure',
                'message': message
            }, status=422)
        except Exception as exc:
            print(exc)
            return JsonResponse({
                'status': 'Failure',
                'message': 'Somethink went wrong while processing the request'
            }, status=500)
    return inner
