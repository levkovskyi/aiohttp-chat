import json


def error_json(message):
    return json.dumps({'error': message})
