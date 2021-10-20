# app/models/models.py
# Document models

from mongoengine import Document, StringField


class User(Document):
    """User model"""

    # User register fields
    email = StringField(required=True)
    first_name = StringField(required=True)
    last_name = StringField(required=True)
    password = StringField(required=True)
    # Database alias used to connect (mongoengine format)
    meta = {"db_alias": "user"}
