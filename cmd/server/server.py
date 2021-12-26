import argparse

from flask import Blueprint, current_app, jsonify
from novaclient import exceptions as nova_exceptions
from novaclient import client

from objects import message

bp = Blueprint('server', __name__, url_prefix='/servers')

NOVA_VERSION = '2'


@bp.route('', methods=['POST'])
def show():
    options = []
    envs = current_app.config['ENVS']
    for env in envs:
        name = env.replace(':', ' ')
        options.append(message.Option(name, env))

    action = message.Action(name='Environments',
                            text="Select an Environment",
                            action_type='select',
                            options=options)

    resp = message.Response(response_type='inChannel', text='서버 조회')
    resp.attachments = [message.Attachment(actions=[action])]

    return jsonify(resp.to_dict())


def callback(args_str: str, **kwargs):
    parser = argparse.ArgumentParser()
    parser.add_argument('server_id', type=str)
    args = parser.parse_args(args_str.split())

    env = kwargs.get('Environments')
    opts = current_app.config.get(env)

    nova = client.Client(NOVA_VERSION, auth_url=opts.get('auth_url'),
                         username=opts.get('username'),
                         password=opts.get('password'),
                         project_id=opts.get('project_id'),
                         region_name='KR1')

    resp = message.Response(response_type='inChannel', text='조회 결과:\n',
                            replace_original=True)

    try:
        print(args.server_id)
        srv = nova.servers.get(args.server_id)
        print(srv.__dict__)
        print(dir(srv))

        # resp.text += '\n```\n' + str(srv) + '\n```'

        fields = [message.Field(title='Name', value=srv.name),
                  message.Field(title='ID', value=srv.id),
                  message.Field(title='Status', value=srv.status),
                  message.Field(title='OS-EXT-STS:vm_state', value=getattr(srv, 'OS-EXT-STS:vm_state'), short=True),
                  message.Field(title='OS-EXT-STS:task_state',
                                value=str(getattr(srv, 'OS-EXT-STS:task_state', 0)), short=True)]

        resp.attachments = [message.Attachment(fields=fields)]
    except nova_exceptions.ClientException as e:
        resp.text += '({code}) {msg}'.format(code=e.code, msg=e.message)
        return jsonify(resp.to_dict())

    return jsonify(resp.to_dict())
