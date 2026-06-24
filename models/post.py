import uuid
from datetime import datetime, timezone

from mongoengine import Document, ListField, StringField, IntField, DateTimeField, UUIDField


class Post(Document):
    id = UUIDField(primary_key=True, default=uuid.uuid4, binary=False)
    title = StringField(required=True, max_length=300)
    content = StringField(default="")
    image = StringField(default="")
    authorId = StringField(required=True)
    authorName = StringField(default="")
    authorAvatar = StringField(default="")
    eventId = StringField(default="")
    likes = IntField(default=0)
    likedBy = ListField(StringField(), default=[])
    status = StringField(default="draft")
    publishedAt = DateTimeField(default=None, null=True)
    createdAt = DateTimeField(default=lambda: datetime.now(timezone.utc))

    meta = {"collection": "posts"}
