import uuid
from datetime import datetime, timezone

from mongoengine import Document, StringField, DateTimeField, UUIDField


class Meeting(Document):
    id = UUIDField(primary_key=True, default=uuid.uuid4, binary=False)
    title = StringField(required=True, max_length=300)
    date = StringField(default="")
    time = StringField(default="")
    description = StringField(default="")
    postId = StringField(default="")
    eventId = StringField(default="")
    participants = StringField(default="")
    status = StringField(default="scheduled")
    authorId = StringField(required=True)
    authorName = StringField(default="")
    createdAt = DateTimeField(default=lambda: datetime.now(timezone.utc))

    meta = {"collection": "meetings"}
