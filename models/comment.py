import uuid
from datetime import datetime, timezone

from mongoengine import Document, StringField, DateTimeField, UUIDField


class Comment(Document):
    id = UUIDField(primary_key=True, default=uuid.uuid4, binary=False)
    postId = StringField(default="")
    eventId = StringField(default="")
    parentId = StringField(default="")
    authorId = StringField(default="")
    authorName = StringField(default="")
    authorAvatar = StringField(default="")
    content = StringField(required=True)
    timestamp = DateTimeField(default=lambda: datetime.now(timezone.utc))

    meta = {"collection": "comments"}
