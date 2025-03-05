""" Adapted from: https://flask-jwt-extended.readthedocs.io/en/stable/automatic_user_loading.html """
from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, current_user, get_jwt_identity, jwt_required

from jwtexample.models import User

bp = Blueprint('main', __name__)


# Create a route to authenticate your users and return JWTs.
# The create_access_token() function is used to actually generate the JWT.
@bp.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    user = User.query.filter_by(username=username).one_or_none()
    if not user or not user.check_password(password):
        return jsonify("Wrong username or password"), 401

    # Notice that we are passing in the actual sqlalchemy user object here
    access_token = create_access_token(identity=user)
    return jsonify(access_token=access_token)


# Protect a route with jwt_required, which will kick out requests
# without a valid JWT present.
@bp.route("/who_am_i", methods=["GET"])
@jwt_required()
def who():
    # We can now access our sqlalchemy User object via `current_user`.
    return jsonify(
        id=current_user.id,
        username=current_user.username,
    )

# Protect a route with jwt_required, which will kick out requests
# without a valid JWT present.
@bp.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

# You will also need to add routes to register a new user and to logout