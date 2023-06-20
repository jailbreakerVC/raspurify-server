from flask import Flask

# Create an instance of the Flask class
app = Flask(__name__)

# Define a route and its corresponding handler function


@app.route('/', methods=["GET"])
def hello():
    return 'Hello, World!'


# Run the Flask application
if __name__ == '__main__':
    app.run(port=3000)
