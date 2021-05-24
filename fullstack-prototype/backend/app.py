from flask import Flask, jsonify
import mysql.connector

app = Flask(__name__)


@app.route('/')
def hello_world():
    connection = mysql.connector.connect(
        host="database",
        user="root",
        password="p@ssw0rd1",
        database="Astronomy"
    )

    cursor = connection.cursor()

    cursor.execute("SELECT * FROM Reports")

    results = cursor.fetchall()

    cursor.close()

    return jsonify(results)


if __name__ == '__main__':
    app.run()
