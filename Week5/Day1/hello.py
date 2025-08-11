from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello_world():
    """
    Return a friendly greeting from the entire team at hello world
    prod.
    """

    return "Hello World"


if __name__ == "__main__":
    app.run()
