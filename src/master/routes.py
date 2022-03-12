from flask import Flask, request

app = Flask(__name__)


def run():
    app.run(debug=True)


@app.get("/get/<argument>")
def print_something(argument):
    return f"{argument}"


@app.post('/post/')
def post():
    print(request.json['clef'])
    return ""
