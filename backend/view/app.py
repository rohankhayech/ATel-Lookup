import mysql.connector
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
