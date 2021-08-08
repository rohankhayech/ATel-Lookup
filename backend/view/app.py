import os
from model.db_helper import (
    add_admin_user,
    get_hashed_password,
    UserNotFoundError,
    ExistingUserError,
)
from flask import Flask, jsonify, request
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    current_user,
    jwt_required,
)
from werkzeug.security import check_password_hash, generate_password_hash

from model.db_helper import init_db

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


@app.route("/signup", methods=["POST"])
def signup():
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    try:
        add_admin_user(
            username=email,
            password=generate_password_hash(password),
        )

        return login()
    except ExistingUserError:
        return "Username is taken", 400
    except ValueError:
        return "Invalid values", 400


@app.route("/login", methods=["POST"])
def login():
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    try:
        hashed = get_hashed_password(username=email)
        if not check_password_hash(hashed, password):
            return "Invalid credentials", 401

        access_token = create_access_token(identity=email)
        return access_token
    except UserNotFoundError:
        return jsonify("Invalid credentials"), 401


@app.route("/user", methods=["GET"])
@jwt_required()
def protected():
    return current_user


if __name__ == "__main__":
    app.run()
