import configparser
import os

from flask import Flask, request, jsonify, Response

from cmd.cluster import cluster
from cmd.server import server
from objects import message

app = Flask(__name__, static_folder=None)

app.register_blueprint(server.bp)
app.register_blueprint(cluster.bp)


@app.route('/monitor/l7check', methods=['GET'])
def check():  # put application's code here
    return Response(status=200)


@app.route('/callback', methods=['POST'])
def webhook():
    print(request.get_json())
    cb = message.Callback.from_dict(request.get_json())

    resp = None
    if cb.command == '/server':
        resp = server.callback(cb.args, **{cb.action_name: cb.action_value})
    elif cb.command == '/cluster':
        resp = cluster.callback(cb.args, **{cb.action_name: cb.action_value})

    return resp if resp else Response(status=400, response='Not Found Commands')


if __name__ == '__main__':
    config_file = os.path.join(os.path.dirname(__file__), '.', os.getenv("CONFIG_FILE"))
    parser = configparser.ConfigParser()
    parser.read(config_file)

    envs = []
    for section in parser.sections():
        if not section.startswith('ENV:'):
            continue
        env = section.split(':', maxsplit=1)[1]
        envs.append(env)
        app.config[env] = dict(parser.items(section))
    app.config['ENVS'] = envs

    host = parser.get('default', 'addr')
    port = parser.getint('default', 'port')

    app.run(host=host, port=port)
