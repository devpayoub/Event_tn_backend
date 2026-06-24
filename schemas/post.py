from pydantic import BaseModel


class PostCreate(BaseModel):
    title: str
    content: str = ""
    image: str = ""
    eventId: str = ""
    status: str = "draft"


class PostUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
    image: str | None = None
    eventId: str | None = None
    status: str | None = None
    likes: int | None = None

    def model_dump(self, *args, **kwargs):
        data = super().model_dump(*args, **kwargs)
        if "likes" in data and data["likes"] is None:
            del data["likes"]
        return data


class PostResponse(BaseModel):
    id: str
    title: str
    content: str
    image: str
    authorId: str
    authorName: str
    authorAvatar: str
    eventId: str
    likes: int
    likedBy: list[str]
    status: str
    publishedAt: str | None
    createdAt: str
