from mongoengine import Document, StringField, DateTimeField
from datetime import datetime, timezone


class User(Document):
    username = StringField(required=True, unique=True, max_length=100)
    email = StringField(required=True, unique=True, max_length=200)
    password = StringField(required=True)
    role = StringField(default="Event Contributor", max_length=100)
    bio = StringField(default="")
    avatar = StringField(
        default="https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=150&h=150&q=80"
    )
    created_at = DateTimeField(default=lambda: datetime.now(timezone.utc))

    meta = {"collection": "users"}
