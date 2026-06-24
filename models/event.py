import uuid
from datetime import datetime, timezone

from mongoengine import Document, StringField, DateTimeField, UUIDField


class Event(Document):
    id = UUIDField(primary_key=True, default=uuid.uuid4, binary=False)
    title = StringField(required=True, max_length=300)
    description = StringField(default="")
    date = StringField(default="")
    time = StringField(default="")
    location = StringField(default="")
    coverImage = StringField(default="")
    ticketUrl = StringField(default="")
    status = StringField(default="draft")
    authorId = StringField(required=True)
    authorName = StringField(default="")
    createdAt = DateTimeField(default=lambda: datetime.now(timezone.utc))

    meta = {"collection": "events"}
