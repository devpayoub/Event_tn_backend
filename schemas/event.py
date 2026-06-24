from pydantic import BaseModel


class EventCreate(BaseModel):
    title: str
    description: str = ""
    date: str = ""
    time: str = ""
    location: str = ""
    coverImage: str = ""
    ticketUrl: str = ""
    status: str = "draft"


class EventUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    date: str | None = None
    time: str | None = None
    location: str | None = None
    coverImage: str | None = None
    ticketUrl: str | None = None
    status: str | None = None


class EventResponse(BaseModel):
    id: str
    title: str
    description: str
    date: str
    time: str
    location: str
    coverImage: str
    ticketUrl: str
    status: str
    authorId: str
    authorName: str
    createdAt: str
