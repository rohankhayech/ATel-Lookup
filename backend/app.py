from typing import Tuple

import flask
import mysql.connector
import json
import jwt
from datetime import datetime
from flask import Flask, jsonify
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
    login,
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
def enter_credentials():
    '''Validate user input and call login() function.
    
    Args:
        credentials (json): A JSON object representing a username and password.

    Returns:
        json: JSON authentication token.

    '''
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    try:
        return login(username, password)
    except InvalidCredentialsError:
        return jsonify("Invalid credentials"), 401
    except UserNotFoundError:
        return jsonify("Invalid credentials"), 401


@app.route("/user", methods=["GET"])
@jwt_required()
def get_user():
    """
    Return the email of the current user if they are authenticated.

    Returns:
        string: The email address of the current user
    """
    return current_user


if __name__ == "__main__":
    app.run()




#Tully's Pulbic Web Interface Functions

def imports(json: json) -> json:
    '''Called by the web interface with the flag auto or manual (determining 
    whether a specific report is to be added, or to just import any new reports since last import)

    Args:
        json (json): A JSON object. See SAS for breakdown of objects fields.
    
    Returns:
        json: JSON flag – Flag that states whether the import was successful or unsuccessful. 

    '''
    return 0 #stub


def search(json: json) -> json:
    '''The purpose of this function is to help with the actual searching aspect of our system, 
    it will be called by the submit search form, and will call the either of the search functions 
    in the search module, as well as both visualisation functions. 

    Args:
        json (json): a JSON object containing relevant fields. See SAS for breakdown of fields.
    
    Returns:
        bool: determines whether the search was successful.
        reports_list: a list of ATel reports returned by search queries. 
        nodes_list: a list of report nodes for the visualisation graph. 
        edges_list: a list of edges for the visualisation graph.  

    '''
    return 0 #stub


def load_metadata() -> Tuple[datetime, int]:
    '''To get the data associated with imports, such as the last time 
    it was updated and how many reports we have.
    
    Returns:
        datetime: A Python datetime object specifying the last updated date for the database.

        int: integer – Count of reports in the database (this number is also the last ATel 
            number we have stored, as ATel reports are numbered increasingly)

    '''
    return datetime.datetime, 0 #stub


def encode_auth_token(self, username_in):
    """
    Generates the Auth Token
    :return: string
    """
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=5),
            'iat': datetime.datetime.utcnow(),
            'sub': username_in
        }
        return jwt.encode(
            payload,
            app.config.get('SECRET_KEY'),
            algorithm='HS256'
        )
    except Exception as e:
        return e