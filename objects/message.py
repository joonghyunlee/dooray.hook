from typing import List


class Option:
    def __init__(self, text=None, value=None):
        self.text = text
        self.value = value

    def to_dict(self):
        return {'text': self.text, 'value': self.value}


class Action(object):
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


class Field(object):
    def __init__(self, title=None, value=None, short=False):
        self.title = title
        self.value = value
        self.short = short

    def to_dict(self):
        return {'title': self.title,
                'value': self.value,
                'short': self.short}


class Attachment:
    def __init__(self,
                 callback_id=None,
                 text=None,
                 title_link=None,
                 author_name=None,
                 author_link=None,
                 image_url=None,
                 thumb_url=None,
                 fields: List[Field] = None,
                 actions: List[Action] = None):
        self.callback_id = callback_id
        self.text = text
        self.title_link = title_link
        self.author_name = author_name
        self.author_link = author_link
        self.image_url = image_url
        self.thumb_url = thumb_url
        self.fields = fields if fields else []
        self.actions = actions if actions else []

    def to_dict(self):
        return {'callbackId': self.callback_id,
                'fields': [field.to_dict() for field in self.fields],
                'actions': [action.to_dict() for action in self.actions]}


class Response:
    def __init__(self, response_type=None, text=None,
                 replace_original=False, attachments=None):
        self.response_type = response_type
        self.text = text
        self.replace_original = replace_original
        self.attachments = attachments if attachments else []

    def to_dict(self):
        return {'responseType': self.response_type,
                'replaceOriginal': self.replace_original,
                'text': self.text,
                'attachments': [attachment.to_dict() for attachment in self.attachments]}


class Request(object):
    def __init__(self, tenant_id=None,
                 tenant_domain=None,
                 channel_id=None,
                 channel_name=None,
                 user_id=None,
                 user_name=None,
                 command=None,
                 text=None,
                 response_url=None,
                 app_token=None,
                 cmd_token=None,
                 trigger_id=None):
        self.tenant_id = tenant_id
        self.tenant_domain = tenant_domain
        self.channel_id = channel_id
        self.channel_name = channel_name
        self.user_id = user_id
        self.user_name = user_name
        self.command = command
        self.text = text
        self.response_url = response_url
        self.app_token = app_token
        self.cmd_token = cmd_token
        self.trigger_id = trigger_id

    @classmethod
    def from_dict(cls, value):
        return Request(tenant_id=value.get('tenantId'),
                       tenant_domain=value.get('tenantDomain'),
                       channel_id=value.get('channelId'),
                       channel_name=value.get('channelName'),
                       user_id=value.get('userId'),
                       user_name=value.get('userName'),
                       command=value.get('command'),
                       text=value.get('text'),
                       response_url=value.get('responseUrl'),
                       app_token=value.get('appToken'),
                       cmd_token=value.get('cmdToken'),
                       trigger_id=value.get('triggerId'))


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
