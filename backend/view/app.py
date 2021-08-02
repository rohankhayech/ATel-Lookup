import mysql.connector
from flask import Flask, jsonify


app = Flask(__name__)


@app.route("/")
def index():
    connection = mysql.connector.connect(
        host="database", user="root", password="p@ssw0rd1", database="Astronomy"
    )

    cursor = connection.cursor()

    cursor.execute("SELECT * FROM Reports")

    results = cursor.fetchall()

    cursor.close()

    return jsonify(results)


if __name__ == "__main__":
    app.run()
