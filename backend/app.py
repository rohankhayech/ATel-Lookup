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

from model.ds.search_filters import SearchFilters, DateFilter
from model.ds.report_types import ReportResult
from model.constants import FIXED_KEYWORDS
from typing import Tuple

import json
import jwt
from datetime import datetime
from flask import Flask, jsonify, request
from flask_cors import CORS
import os

from controller.importer.importer import *
from controller.search.search import *
from astropy.coordinates import SkyCoord
from view.web_interface import *
from view.vis import *




from flask_jwt_extended import (
    JWTManager,
    current_user,
    jwt_required,
)

from model.db.db_interface import UserNotFoundError
from model.db.db_init import init_db
from controller.authentication import (
    InvalidCredentialsError,
    login,
)

from multiprocessing import Process
from NamedAtomicLock import NamedAtomicLock

lock = NamedAtomicLock("importr")

app = Flask(__name__)
jwt = JWTManager(app)
CORS(app)

app.config["JWT_SECRET_KEY"] = os.environ["JWT_SECRET_KEY"]


@app.route("/")
def index():
    return jsonify("")


"""
Authentication Endpoints

Author:
    Greg Lahaye
"""


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


"""
Web Interface Endpoints

Author:
    Tully Slattery
"""


@app.route("/import", methods=["POST"])
def imports() -> json:
    """Called by the web interface with the flag auto or manual (determining
    whether a specific report is to be added, or to just import any new reports since last import)

    Args:
        json (json): A JSON object. See SAS for breakdown of objects fields.

    Returns:
        json: JSON flag – Flag that states whether the import was successful or unsuccessful.

    """

    # print("REQUEST.JSON PRINTOUT -> ", request.json)
    # set initial flag
    flag = 1
    message = ""

    # retrieve json imports
    import_mode_in = request.json.get("import_mode", None)
    atel_num_in = request.json.get("atel_num", None)

    if import_mode_in != "manual" and import_mode_in != "auto":  # check if import mode not named correctly
        flag = 0
        message = "Import mode was not manual or auto"
    elif import_mode_in == "manual" and valid_atel_num(atel_num_in) == False:  # check if import mode set to manual but correct atel number was not provided
        flag = 2
        message = "The ATel number provided is invalid"

    if flag == 1: # if all tests have passed so far
        try:
            if import_mode_in == "manual":
                import_report(atel_num_in) # call manual import
            elif import_mode_in == "auto":
                background_import()
        except ReportAlreadyExistsError as e:
            flag = 2
            message = str(e)
        except ReportNotFoundError as e:
            flag = 2
            message = str(e)
        except ImportFailError as e:
            flag = 0
            message = str(e)
        except MissingReportElementError as e:
            flag = 0
            message = str(e)

    return jsonify({"flag": flag, "message": message})


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

    '''
    SETTING INITIAL VARIABLES
    '''

    flag = 1 
    message = ""
    reports = []
    list_result = [], []
    report_dicts = []

    start_date_obj = None
    end_date_obj = None
    ra = 0.0
    dec = 0.0
    radius = 10.0
    sky_coord = None

    #retrieving json imports
    term_in = request.json.get("term", None)
    search_mode_in = request.json.get("search_mode", None)
    search_data_in = request.json.get("search_data", None)
    keywords_in = request.json.get("keywords", None)
    keyword_mode_in = request.json.get("keyword_mode", None)
    start_date_in = request.json.get("start_date", None)
    end_date_in = request.json.get("end_date", None)

    # if any fields are missing from the JSON request, flag 0
    try: 
        none_check(term_in, search_mode_in, search_data_in, keywords_in, keyword_mode_in, start_date_in, end_date_in)
    except ValueError as e:
        flag = 0
        message = "Bad JSON request, all fields not recieved"


    '''
    VARIABLE MODIFICATION
    '''

    #If field blank, set to None
    if flag == 1:
        if search_mode_in == "":
            search_mode_in = None
        if search_mode_in == "name" and search_data_in == "":
            search_data_in = None
        if search_mode_in == "coords" and search_data_in == ["","",""]:
            search_data_in = None
        if keywords_in == "" or keywords_in == [""]:
            keywords_in = None
        if keyword_mode_in == "":
            keyword_mode_in = None
        if start_date_in == "":
            start_date_in = None
        if end_date_in == "":
            end_date_in = None
        if term_in == "":
            term_in = None

    # turning dates into date objects
    if flag == 1:
        if start_date_in != None:
            try:
                start_date_obj = parse_date_input(start_date_in)
            except ValueError as e:
                flag = 2
                message = str(e)

    if flag == 1:
        if end_date_in != None:
            try:
                end_date_obj = parse_date_input(end_date_in)
            except ValueError as e:
                flag = 2
                message = str(e)


    # set keywords_in to None if empty
    if flag == 1:
        if keywords_in == []:
            keywords_in = None


    '''
    CHECKS
    '''

    #checking if search_mode_in has a valid value - SEARCH MODE CHECK
    if flag == 1:
        try:
            search_mode_check(search_mode_in)
        except ValueError as e:
            flag = 0 # system error
            message = str(e)


    #checking to make sure atleast one of the required fields has been given - REQUIRED FIELDS CHECK
    if flag == 1:
        try:
            req_fields_check(search_data_in, keywords_in, keyword_mode_in, term_in)
        except ValueError as e:
            flag = 2 # user error
            message = str(e)


    # checking if start date is greater than end date and vice versa - DATE VALIDITY CHECK
    # checking if start date and end date are infact dates in the past - DATE VALIDITY CHECK
    if flag == 1:
        if start_date_obj != None and end_date_obj != None:
            try:
                valid_date_check(start_date_obj, end_date_obj)
            except ValueError as e:
                flag = 2 # user error
                message = str(e)


    #checking if keywords are within the FIXED_KEYWORDS list - KEYWORDS CHECK
    if flag == 1:
        if keyword_mode_in != None and (keywords_in != None and keywords_in != ""):
            try:
                keywords_check(keywords_in)
            except ValueError as e:
                flag = 0 # system error
                message = str(e)



    #creating the keyword_mode enum - KEYWORDS MODE CHECK
    if flag == 1:
        keyword_mode_enum = KeywordMode.ANY
        if keyword_mode_in != None and (keywords_in != None and keywords_in != ""):
            try:
                keyword_mode_check(keyword_mode_in)
                keyword_mode_enum = parse_keyword_mode(keyword_mode_in)
            except ValueError as e:
                flag = 0 # system error
                message = str(e) 


    #performing basic validation on the coordinate search data - COORD DATA CHECK
    if flag == 1:
        if (search_mode_in == "coords" and search_data_in != None and search_data_in != ""):
            try:
                valid_coords_basic_check(search_data_in)
            except ValueError as e:
                flag = 2 # user error
                message = str(e) 

            
            

    '''
    FUNCTIONS AFTER CHECKS COMPLETED
    '''

    #CREATING THE SKYCOORD OBJECT IF THERE ARE COORDS GIVEN
    if flag == 1:
        if (search_mode_in == "coords" and search_data_in != None):  # if the search mode is "coords" need to make sure there is three values given
            if len(search_data_in) == 3:
                ra = search_data_in[0]
                dec = search_data_in[1]
                radius = search_data_in[2]
                if radius == "":
                    radius = 10.0 # default value for radius is 10.0, so if not given, set to 10.0

                try:
                    valid_ra(ra)
                    valid_dec(dec)
                    sky_coord = parse_search_coords(ra,dec)
                except ValueError as e:
                    flag = 2
                    message = str(e)

            else:
                flag = 0 # system error
                message = "Bad JSON request, full coordinates field not provided"


    #CREATING SEARCH FILTERS OBJECT
    if flag == 1:
        if term_in == None and keywords_in == None: # set search filters to None if the term is blank and no keywords were provided
            search_filters = None
        else:
            search_filters = SearchFilters(
                term_in, keywords_in, keyword_mode_enum
            )  # creating the search filters object



    #CREATING DATE FILTERS OBJECT
    if flag == 1:
        if start_date_in == None and end_date_in == None: # set the date filters to None if no dates have been provided
            date_filter = None
        else:
            date_filter = DateFilter(start_date_obj, end_date_obj)



    #CALLING SEARCH REPORTS BY NAME AND SEARCH REPORTS BY COORDS TO GET reports OUTPUT
    if flag == 1:
        if search_mode_in == "coords" and search_data_in == None:
            search_mode_in = "name"
        if search_mode_in == "name":
            try:
                reports = search_reports_by_name(search_filters, date_filter, search_data_in)
            except ValueError as e:
                if hasattr(e, "message"):
                    msg = e.message
                else:
                    msg = str(e)
                flag = 0 #system error
                message = msg
        elif search_mode_in == "coords":
            radius_float = float(radius)
            try:
                valid_radius(radius)
                reports = search_reports_by_coords(search_filters, date_filter, sky_coord, radius_float)
            except ValueError as e:
                flag = 2 # user error
                message = str(e)
            


    #CALLING VISUALISATION FUNCTION TO GET NODES/EDGES LIST RESULT
    if flag == 1:
        list_result = create_nodes_list(reports)
        for report in reports:
            report_dicts.append(
                {
                    "atel_num": report.atel_num,
                    "title": report.title,
                    "authors": report.authors,
                    "body": report.body,
                    "submission_date": str(report.submission_date),
                    "referenced_reports": report.referenced_reports,
                }
            )



    #SEARCH FUNCTION RETURN
    return jsonify(
        {
            "flag": flag,
            "report_list": report_dicts,
            "node_list": list_result[0],
            "edge_list": list_result[1],
            "message": message
        }
    )


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
    last_updated = db.get_last_updated_date()
    next_atel = db.get_next_atel_num()

    return jsonify(
        {"keywords": keywords, "lastUpdated": last_updated, "nextAtel": next_atel}
    )


def background_import():
    process = Process(target=background_import_task, daemon=True)
    process.start()


def background_import_task():
    lock.acquire()
    import_all_reports()
    lock.release()


"""
Application Main Line  
  
"""
# Initialise the database
init_db()

if __name__ == "__main__":
    # Run the application
    app.run()
