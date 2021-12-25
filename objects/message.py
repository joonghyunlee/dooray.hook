class Option:
    def __init__(self, text=None, value=None):
        self.text = text
        self.value = value

    def to_dict(self):
        return {'text': self.text, 'value': self.value}


class Attachment:
    def __init__(self,
                 callback_id=None,
                 actions=None):
        self.callback_id = callback_id
        self.actions = actions

    def to_dict(self):
        return {'callbackId': self.callback_id,
                'actions': [action.to_dict() for action in self.actions]}


class ActionAttachment(object):
    def __init__(self, name=None, text=None, action_type=None, options=None):
        self.name = name
        self.text = text
        self.type = action_type
        self.options = options if options else []

    def to_dict(self):
        return {'name': self.name,
                'text': self.text,
                'type': self.type,
                'options': [option.to_dict() for option in self.options]}


class Response:
    def __init__(self, response_type=None, text=None, attachments=None):
        self.response_type = response_type
        self.text = text
        self.attachments = attachments if attachments else []

    def to_dict(self):
        return {'responseType': self.response_type,
                'text': self.text,
                'attachments': [attachment.to_dict() for attachment in self.attachments]}


class Request(object):
    def __init__(self):
        self.tenant_id = ""
        self.tenant_domain = ""
        self.channel_id = ""
        self.channel_name = ""
        self.user_id = ""
        self.user_name = ""
        self.command = ""
        self.text = ""
        self.response_url = ""
        self.app_token = ""
        self.cmd_token = ""
        self.trigger_id = ""


class Callback(object):
    def __init__(self, command=None,
                 args=None,
                 user_id=None,
                 user_name=None,
                 action_name=None,
                 action_value=None):
        self.command = command
        self.args = args
        self.user_id = user_id
        self.user_name = user_name
        self.action_name = action_name
        self.action_value = action_value

    @classmethod
    def from_dict(cls, value):
        return Callback(command=value.get('command'),
                        args=value.get('text'),
                        user_id=value.get('user').get("id") if 'user' in value else None,
                        user_name=value.get('user').get("name") if 'user' in value else None,
                        action_name=value.get('actionName'),
                        action_value=value.get('actionValue'))

