from umongo import Document, fields

from core.db import mongo_instance


@mongo_instance.register
class User(Document):
    email = fields.EmailField(required=True)
    login = fields.StringField(required=True, unique=True)
    password = fields.StringField(required=True)
