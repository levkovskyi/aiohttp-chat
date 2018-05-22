from datetime import datetime
from umongo import Document, fields

from auth.models import User
from core.db import instance


@instance.register
class Message(Document):
    message = fields.StringField(required=True)
    time = fields.DateTimeField(missing=datetime.now())
    user_id = fields.ReferenceField(User, required=True)

    @property
    def user(self):
        user = self.user_id._document
        return user
