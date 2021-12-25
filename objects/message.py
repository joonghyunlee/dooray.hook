import json


class Attachment:
    def __init__(self,
                 callback_id=None,
                 actions=None,
                 name=None,
                 text=None,
                 attachment_type=None,
                 options=None):
        self.callback_id = callback_id
        self.actions = actions
        self.name = name
        self.text = text
        self.type = attachment_type
        self.options = options

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__)


class Response:
    def __init__(self):
        self.response_type = 'inChannel'
        self.text = 'Hello World'

    def to_dict(self):
        return {'responseType': self.response_type,
                'text': self.text}


class Request(object):
    def __init__(self):
        self.tenant_id = ""
        self.tenant_domain = ""
        self.channel_id = ""
        self.channel_name = ""
        self.user_id = ""
        self.command = ""
        self.text = ""
        self.response_url = ""
        self.app_token = ""
        self.cmd_token = ""
        self.trigger_id = ""
