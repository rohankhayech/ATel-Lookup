"""
The main line of the application's backend.

The purpose of the web interface is to create a link between the other components of the application and perform most of the validation for input data from the user and any data that will be used in calculations.

Author:
    Tully Slattery

Contributors:
    Greg Lahaye

License Terms and Copyright:
    Copyright (C) 2021 Tully Slattery, Greg Lahaye

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program. If not, see <https://www.gnu.org/licenses/>.
"""

from model.ds.search_filters import SearchFilters
from model.ds.report_types import ReportResult
from model.constants import FIXED_KEYWORDS
from typing import Tuple

import flask
import mysql.connector
import json
import jwt
from datetime import datetime
from flask import Flask, jsonify
from flask_cors import CORS
import os

from controller.importer.importer import *
from controller.search.search import * #ImportError: cannot import name 'DEFAULT_RADIUS' from 'model.constants' (/app/model/constants.py)
from astropy.coordinates import SkyCoord
from view.web_interface import *
# from view.vis import * #not working yet 30/08

from flask import Flask, jsonify, request
from flask_jwt_extended import (
    JWTManager,
    current_user,
    jwt_required,
)
import requests

from model.db.db_interface import UserNotFoundError
from model.db.db_init import init_db
from controller.authentication import (
    InvalidCredentialsError,
    login,
)

app = Flask(__name__)
jwt = JWTManager(app)
CORS(app)

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


@app.route("/authenticate", methods=["POST"])
def enter_credentials():
    """Validate user input and call login() function.

    Args:
        credentials (json): A JSON object representing a username and password.

    Returns:
        json: JSON authentication token.

    """
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    try:
        token = login(username, password)
        return jsonify(token)
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


# Web Interface Functions - Tully Slattery


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

    if import_mode_in != "manual" and import_mode_in != "auto": # import mode not named correctly
        flag = 0
    elif import_mode_in == "manual" and atel_num_in is None: # import mode set to manual but atel number was not provided
        flag = 0
    elif import_mode_in == "manual" and atel_num_in <= 0: # atel number not valid
        flag = 0   

    if flag == 1:
        try:
            if import_mode_in == "manual":
                # import_report(atel_num_in) #currently not working, talk to nathan, issue with download_report 28/08/2021 9:39pm
                pass
            elif import_mode_in == "auto":
                import_all_reports() 
        except ReportAlreadyExistsError as e:
            flag = 0
        except ReportNotFoundError as e:
            flag = 0
        pass

    return jsonify({"flag": flag})


@app.route("/search", methods=["POST"])
def search() -> json:
    """The purpose of this function is to help with the actual searching aspect of our system,
    it will be called by the submit search form, and will call the either of the search functions
    in the search module, as well as both visualisation functions.

    Args:
        json (json): a JSON object containing relevant fields. See SAS for breakdown of fields.

    Returns:
        bool: determines whether the search was successful.
        reports_list: a list of ATel reports returned by search queries.
        nodes_list: a list of report nodes for the visualisation graph.
        edges_list: a list of edges for the visualisation graph.

    """

    flag = 1 # set initial flag to success
    reports = []

    search_mode_in = request.json.get("search_mode", None)
    search_data_in = request.json.get("search_data", None)
    keywords_in = request.json.get("keywords", None)
    keyword_mode_in = request.json.get("keyword_mode", None)
    start_date_in = request.json.get("start_date", None)
    end_date_in = request.json.get("end_date", None)

    if start_date_in != None:
        start_date_obj = datetime.strptime(start_date_in,"%Y-%m-%d")
    
    if end_date_in != None:
        end_date_obj = datetime.strptime(end_date_in, "%Y-%m-%d")
    
    
    if search_data_in == None and keywords_in == None and keyword_mode_in == None: # At least one of the text fields (search_data) or keyword boxes (keywords/keyword_mode must be filled).
        flag = 0
    elif start_date_obj > datetime.now() or end_date_obj > datetime.now():
        flag = 0
    elif search_mode_in != "coords" and search_mode_in != "name":
        flag = 0
    elif keyword_mode_in != "none" and keyword_mode_in != "all" and keyword_mode_in != "any" and keyword_mode_in != None:
        flag = 0
    elif start_date_obj > end_date_obj or end_date_obj < start_date_obj:
        flag = 0
    


    if search_mode_in == "coords": # if the search mode is "coords" need to make sure there is three values given
        if len(search_data_in) == 3:
            dec = search_data_in[0]
            ra = search_data_in[1]
            radius = search_data_in[2]
            try:
                sky_coord = SkyCoord(ra,dec,frame='icrs', unit=('deg', 'deg'))
            except ValueError as e:
                flag = 0
        else:
            flag = 0 # if search data is not fit for coords, set flag to failure

    if keyword_mode_in != None:
        for x in keywords_in:
            if x not in FIXED_KEYWORDS:
                flag = 0

    if keyword_mode_in != None:
        if keyword_mode_in == "all":
            keyword_mode_enum = KeywordMode.ALL
        elif keyword_mode_in == "any":
            keyword_mode_enum = KeywordMode.ANY
        elif keyword_mode_in == "none":
            keyword_mode_enum = KeywordMode.NONE

    search_filters = SearchFilters(search_data_in, keywords_in, keyword_mode_enum, start_date_obj, end_date_obj) # creating the search filters object 

    if flag == 1:
        if search_mode_in == "name":
            reports = search_reports_by_name(search_filters, search_data_in) # commented out as search.py produces error with DEFAULT_RADIUS
            pass
        elif search_mode_in == "coords":
            reports = search_reports_by_coords(search_filters, sky_coord, radius) # commented out as search.py produces error with DEFAULT_RADIUS
            pass
        
    if flag == 1:
        # list_result = create_nodes_list(reports) #not implemented yet 30/08
        pass

        # {"flag": flag, "report_list": reports, "nodes_list": list_result}

    if flag == 1:    
        print(reports)


    return jsonify({"flag": flag, "report_list": reports})


@app.route("/metadata", methods=["GET"])
def load_metadata() -> json:
    """To get the data associated with imports, such as the last time
    it was updated and how many reports we have.

    Returns:
        date: in string format.

        int: integer – Count of reports in the database (this number is also the last ATel
            number we have stored, as ATel reports are numbered increasingly)

    """

    keywords = FIXED_KEYWORDS
    last_updated = datetime.now()
    report_count = 0

    return jsonify(
        {"keywords": keywords, "lastUpdated": last_updated, "reportCount": report_count}
    )
