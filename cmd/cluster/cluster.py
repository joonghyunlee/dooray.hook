import argparse

from flask import Blueprint, current_app, jsonify

from keystoneauth1.identity import v2
from keystoneauth1 import session
from magnumclient.client import Client
from magnumclient import exceptions as magnum_exceptions

from objects import message

bp = Blueprint('cluster', __name__, url_prefix='/clusters')


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

    resp = message.Response(response_type='inChannel', text='클러스터 조회')
    resp.attachments = [message.Attachment(actions=[action])]

    return jsonify(resp.to_dict())


def callback(args_str: str, **kwargs):
    parser = argparse.ArgumentParser()
    parser.add_argument('cluster_id', type=str)
    args = parser.parse_args(args_str.split())
    print(args.cluster_id)

    env = kwargs.get('Environments')
    opts = current_app.config.get(env)

    auth = v2.Password(auth_url=opts.get('auth_url'),
                       username=opts.get('username'),
                       password=opts.get('password'),
                       tenant_id=opts.get('project_id'))
    sess = session.Session(auth=auth)
    magnum = Client('1', endpoint_override='https://kr1-api-kubernetes.infrastructure.cloud.toast.com/v1',
                    region_name='KR1', session=sess)

    resp = message.Response(response_type='inChannel', text='조회 결과:\n',
                            replace_original=True)

    try:
        cls = magnum.clusters.get(args.cluster_id)

        fields = [message.Field(title='Name', value=cls.name),
                  message.Field(title='ID', value=cls.uuid),
                  message.Field(title='Status', value=cls.status, short=True),
                  message.Field(title='Reason', value=getattr(cls, 'status_reason', 'None'), short=True),
                  message.Field(title='API Address', value=cls.api_address)]

        resp.attachments = [message.Attachment(fields=fields)]
    except magnum_exceptions.HttpError as e:
        resp.text += '({code}) {msg}'.format(code=e.http_status, msg=e.message)
        return jsonify(resp.to_dict())

    return jsonify(resp.to_dict())
