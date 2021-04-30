from flask import Flask
import flask_monitoringdashboard as dashboard

import time

app = Flask(__name__)

dashboard.bind(app)


@app.route("/")
def hello_world():
    return "Hello, World!"


@app.route("/slow")
def slow():
    time.sleep(2)
    return "Done!"


if __name__ == "__main__":
    app.run(debug=True)
