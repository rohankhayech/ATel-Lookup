from typing import Tuple
import mysql.connector
import json
import jwt
from datetime import datetime
from flask import Flask, jsonify

from model.db_helper import init_db

app = Flask(__name__)

#Initialise the database
init_db()

@app.route("/")
def index():


    return jsonify("")


if __name__ == "__main__":
    app.run()




#Tully's Pulbic Web Interface Functions

def enter_credentials(credentials: json) -> json:
    '''Validate user input and call login() function.
    
    Args:
        credentials (json): A JSON object representing a username and password.

    Returns:
        json: JSON authentication token.

    '''
    #loading imported credentials
    json_object = json.loads(credentials)

    #parsing JSON object into string username and password
    username_in = json_object["username"]
    password_in = json_object["password"]


    #username validation


    #password validation


    #If username is valid and password is valid, call login() from authentication module
    #login(username_in, password_in)
    

    #generate JSON auth token
    json_auth_token = encode_auth_token(username_in)



    return json_auth_token #stub


def imports(json: json) -> json:
    '''Called by the web interface with the flag auto or manual (determining 
    whether a specific report is to be added, or to just import any new reports since last import)

    Args:
        json (json): A JSON object. See SAS for breakdown of objects fields.
    
    Returns:
        json: JSON flag – Flag that states whether the import was successful or unsuccessful. 

    '''
    return 0 #stub


def search(json: json) -> Tuple[bool, list[reports_list], list[nodes_list], list[edges_list]]:
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
    return True, [], [], [] #stub


def load_metadata() -> Tuple[datetime, int]:
    '''To get the data associated with imports, such as the last time 
    it was updated and how many reports we have.
    
    Returns:
        datetime: A Python datetime object specifying the last updated date for the database.

        int: integer – Count of reports in the database (this number is also the last ATel 
            number we have stored, as ATel reports are numbered increasingly)

    '''
    return 1/1/2000, 0 #stub


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