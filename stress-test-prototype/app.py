from flask import Flask
import random
import requests

app = Flask(__name__)


@app.route('/')
def hello_world():
    if random.random() < 0.05:  # randomly fail
        return 'error', 500

    status = do_work()
    return 'result', status


def do_work():
    response = requests.get('https://jsonplaceholder.typicode.com/todos/1')
    return response.status_code
