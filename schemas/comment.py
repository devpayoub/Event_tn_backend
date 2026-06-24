from pydantic import BaseModel, model_validator


class CommentCreate(BaseModel):
    postId: str = ""
    eventId: str = ""
    parentId: str | None = None
    content: str

    @model_validator(mode="after")
    def validate_comment(self):
        if not self.content.strip():
            raise ValueError("Content cannot be empty")
        if not self.postId and not self.eventId:
            raise ValueError("Must provide postId or eventId")
        return self


class CommentUpdate(BaseModel):
    content: str | None = None


class CommentResponse(BaseModel):
    id: str
    postId: str
    eventId: str
    parentId: str | None
    authorId: str
    authorName: str
    authorAvatar: str
    content: str
    timestamp: str
