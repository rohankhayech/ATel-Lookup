import os

from flask import Flask, jsonify, request
from flask_jwt_extended import (
    JWTManager,
    current_user,
    jwt_required,
)

from model.db_helper import UserNotFoundError, init_db
from controller.authentication.authentication import (
    InvalidCredentialsError,
    enter_credentials,
)

app = Flask(__name__)
jwt = JWTManager(app)

app.config["JWT_SECRET_KEY"] = os.environ["JWT_SECRET_KEY"]

# Initialise the database
init_db()


@app.route("/")
def index():
    return jsonify("")


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return identity


@app.route("/login", methods=["POST"])
def login():
    """
    Creates an access token if given credentials are valid.
    """
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    try:
        return enter_credentials(username, password)
    except InvalidCredentialsError:
        return jsonify("Invalid credentials"), 401
    except UserNotFoundError:
        return jsonify("Invalid credentials"), 401


@app.route("/user", methods=["GET"])
@jwt_required()
def get_user():
    """
    Return the email of the current user if they are authenticated.
    """
    return current_user


if __name__ == "__main__":
    app.run()
