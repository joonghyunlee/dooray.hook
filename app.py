from flask import Flask, request, jsonify

from objects import message

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route("/commands", methods=["POST"])
def command():
    print(request.get_json())
    resp = message.Response()
    return jsonify(resp.to_dict())


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
