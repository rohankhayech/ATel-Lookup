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
import requests

from model.db_helper import UserNotFoundError, init_db
from controller.authentication.authentication import (
    InvalidCredentialsError,
    login,
)

app = Flask(__name__)
jwt = JWTManager(app)

# app.config["JWT_SECRET_KEY"] = os.environ["JWT_SECRET_KEY"]
app.config["JWT_SCRET_KEY"] = os.environ["JWT_SECRET_KEY"]

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

@app.route("/import", methods=["POST"])
def imports() -> json:
    '''Called by the web interface with the flag auto or manual (determining 
    whether a specific report is to be added, or to just import any new reports since last import)

    Args:
        json (json): A JSON object. See SAS for breakdown of objects fields.

    Returns:
        json: JSON flag – Flag that states whether the import was successful or unsuccessful. 

    '''
    # print("REQUEST.JSON PRINTOUT -> ", request.json)
    flag = 1

    import_mode_in = request.json.get("import_mode", None)
    atel_num_in = request.json.get("atel_num", None)

    if import_mode_in != "manual" and import_mode_in != "auto":
        flag = 0
    elif import_mode_in == "manual" and atel_num_in is None:
        flag = 0

    if flag == 1:
        # try:
        #     if import_mode_in == "manual":
        #         importreport()
        #     elif import_mode_in == "auto":
        #         importallreports()
        # except ReportAlreadyExistsException as e:
        #     flag = 0
        # except ReportNotFoundException as e:
        #     flag = 0
        pass

    return jsonify({"flag": flag})


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
    return jsonify("") #stub


def load_metadata() -> json:
    '''To get the data associated with imports, such as the last time 
    it was updated and how many reports we have.
    
    Returns:
        date: in string format.

        int: integer – Count of reports in the database (this number is also the last ATel 
            number we have stored, as ATel reports are numbered increasingly)

    '''
    return jsonify("") #stub


