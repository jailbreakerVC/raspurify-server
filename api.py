from flask import Flask
import socket


hostname = socket.gethostbyname('Mac-mini.local')
app = Flask(__name__)


@app.route('/', methods=["GET"])
def hello():
    return 'Hello, World!'


if __name__ == '__main__':
    app.run(port=3000, host=hostname)
