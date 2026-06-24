from math import ceil

from fastapi import APIRouter, Depends, HTTPException, Query, status

from dependencies import get_current_user, optional_current_user
from models.event import Event
from models.user import User
from schemas.common import PaginatedResponse
from schemas.event import EventCreate, EventResponse, EventUpdate

router = APIRouter(prefix="/api/events", tags=["Events"])


def _event_to_response(e: Event) -> EventResponse:
    return EventResponse(
        id=str(e.id),
        title=e.title,
        description=e.description,
        date=e.date,
        time=e.time,
        location=e.location,
        coverImage=e.coverImage or "",
        ticketUrl=e.ticketUrl or "",
        status=e.status or "draft",
        authorId=e.authorId,
        authorName=e.authorName,
        createdAt=e.createdAt.isoformat() if e.createdAt else "",
    )


@router.get("", response_model=PaginatedResponse)
def list_events(
    _user: User | None = Depends(optional_current_user),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=0, le=100),
):
    qs = Event.objects()
    if not _user:
        qs = qs.filter(status__ne="draft")
    total = qs.count()
    effective = limit if limit > 0 else total
    pages = ceil(total / effective) if total > 0 and effective > 0 else 1
    cur_page = (skip // limit) + 1 if limit > 0 else 1
    qs = qs.order_by("-createdAt")
    if effective > 0:
        qs = qs.skip(skip).limit(effective)
    items = [_event_to_response(e) for e in qs]
    return PaginatedResponse(items=items, total=total, page=cur_page, pages=pages)


@router.post("", response_model=EventResponse, status_code=status.HTTP_201_CREATED)
def create_event(body: EventCreate, current_user: User = Depends(get_current_user)):
    event = Event(
        title=body.title,
        description=body.description,
        date=body.date,
        time=body.time,
        location=body.location,
        coverImage=body.coverImage,
        ticketUrl=body.ticketUrl,
        status=body.status,
        authorId=str(current_user.id),
        authorName=current_user.username,
    )
    event.save()
    return _event_to_response(event)


@router.get("/{event_id}", response_model=EventResponse)
def get_event(event_id: str, _user: User | None = Depends(optional_current_user)):
    event = Event.objects(id=event_id).first()
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
    return _event_to_response(event)


@router.patch("/{event_id}", response_model=EventResponse)
def update_event(event_id: str, body: EventUpdate, current_user: User = Depends(get_current_user)):
    event = Event.objects(id=event_id).first()
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
    if str(event.authorId) != str(current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    update_data = body.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(event, key, value)
    event.save()
    return _event_to_response(event)


@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_event(event_id: str, current_user: User = Depends(get_current_user)):
    event = Event.objects(id=event_id).first()
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
    if str(event.authorId) != str(current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    event.delete()
