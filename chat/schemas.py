from marshmallow import fields

from chat.models import Message


class MessageSchema(Message.schema.as_marshmallow_schema()):
    time = fields.DateTime(format='%H:%M:%S')
    user = fields.Method("get_user")

    def get_user(self, obj):
        user = obj.user
        return user.login

    class Meta:
        fields = ('message', 'time', 'user')
