from flask import Blueprint, jsonify, request

auth = Blueprint('auth', __name__)


@auth.route('/signin', methods=['POST'])
def signin():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    access_token, refresh_token = ('', '')
    return jsonify(access_token=access_token, refresh_token=refresh_token)
