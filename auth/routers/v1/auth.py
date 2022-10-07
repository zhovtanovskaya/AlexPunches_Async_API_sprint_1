from flask import Blueprint, jsonify

auth = Blueprint('auth', __name__,)


@auth.route("/login")
def login():
    # auth_data = request.authorization
    return jsonify(hello='')
