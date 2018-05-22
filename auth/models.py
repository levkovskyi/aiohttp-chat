from umongo import Document, fields

from core.db import instance


@instance.register
class User(Document):
    email = fields.EmailField(required=True)
    login = fields.StringField(required=True, unique=True)
    password = fields.StringField(required=True)
