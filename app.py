import configparser
import json
import os

import yaml
from flask import Flask, request, jsonify

from objects import message

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route("/servers", methods=["POST"])
def command():
    print(request.get_json())
    resp = message.Response(response_type='inChannel', text='TEST')

    options = [
        message.Option('KR1', 'KR1'),
        message.Option('KR2', 'KR2'),
        message.Option('JP1', 'JP1'),
        message.Option('US1', 'US1'),
    ]
    action = message.ActionAttachment(name='Region',
                                      text="Select a Region",
                                      action_type='select',
                                      options=options)
    resp.attachments = [message.Attachment(actions=[action])]
    print(resp.to_dict())

    return jsonify(resp.to_dict())


@app.route("/callback", methods=["POST"])
def webhook():
    print(request.get_json())
    cb = message.Callback.from_dict(request.get_json())
    resp = message.Response(response_type='inChannel', text=cb.action_value)
    return jsonify(resp.to_dict())


if __name__ == '__main__':
    config_file = os.path.join(os.path.dirname(__file__), '.', os.getenv("CONFIG_FILE"))
    parser = configparser.ConfigParser()
    parser.read(config_file)

    print(parser.items('KR1:ALPHA'))
    print(type(parser.items('KR1:ALPHA')))
    print(parser.sections())

    app.run(host="0.0.0.0", port=8080)

