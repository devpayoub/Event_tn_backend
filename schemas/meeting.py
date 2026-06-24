from pydantic import BaseModel


class MeetingCreate(BaseModel):
    title: str
    date: str = ""
    time: str = ""
    description: str = ""
    postId: str = ""
    eventId: str = ""
    participants: str = ""
    status: str = "scheduled"


class MeetingUpdate(BaseModel):
    title: str | None = None
    date: str | None = None
    time: str | None = None
    description: str | None = None
    postId: str | None = None
    eventId: str | None = None
    participants: str | None = None
    status: str | None = None


class MeetingResponse(BaseModel):
    id: str
    title: str
    date: str
    time: str
    description: str
    postId: str
    eventId: str
    participants: str
    status: str
    authorId: str
    authorName: str
    createdAt: str
