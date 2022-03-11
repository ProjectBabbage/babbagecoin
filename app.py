from flask import Flask, request

app = Flask(__name__)


@app.get("/get/<argument>")
def print_something(argument):
    return f"{argument}"

@app.post('/post/')
def post():
    print(request.json['clef'])
    return ""

if __name__ == '__main__':
    app.run(debug=True)
