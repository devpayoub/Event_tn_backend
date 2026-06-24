from fastapi import APIRouter, Depends, HTTPException, status

from dependencies import get_current_user, optional_current_user
from models.meeting import Meeting
from models.user import User
from schemas.meeting import MeetingCreate, MeetingResponse, MeetingUpdate

router = APIRouter(prefix="/api/meetings", tags=["Meetings"])


def _meeting_to_response(m: Meeting) -> MeetingResponse:
    return MeetingResponse(
        id=str(m.id),
        title=m.title,
        date=m.date,
        time=m.time,
        description=m.description or "",
        postId=m.postId or "",
        eventId=m.eventId or "",
        participants=m.participants or "",
        status=m.status or "scheduled",
        authorId=m.authorId,
        authorName=m.authorName,
        createdAt=m.createdAt.isoformat() if m.createdAt else "",
    )


@router.get("", response_model=list[MeetingResponse])
def list_meetings(postId: str | None = None, _user: User | None = Depends(optional_current_user)):
    qs = Meeting.objects()
    if postId:
        qs = qs.filter(postId=postId)
    return [_meeting_to_response(m) for m in qs.order_by("-createdAt")]


@router.post("", response_model=MeetingResponse, status_code=status.HTTP_201_CREATED)
def create_meeting(body: MeetingCreate, current_user: User = Depends(get_current_user)):
    meeting = Meeting(
        title=body.title,
        date=body.date,
        time=body.time,
        description=body.description,
        postId=body.postId,
        eventId=body.eventId,
        participants=body.participants,
        status=body.status,
        authorId=str(current_user.id),
        authorName=current_user.username,
    )
    meeting.save()
    return _meeting_to_response(meeting)


@router.get("/{meeting_id}", response_model=MeetingResponse)
def get_meeting(meeting_id: str, _user: User | None = Depends(optional_current_user)):
    meeting = Meeting.objects(id=meeting_id).first()
    if not meeting:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meeting not found")
    return _meeting_to_response(meeting)


@router.patch("/{meeting_id}", response_model=MeetingResponse)
def update_meeting(meeting_id: str, body: MeetingUpdate, current_user: User = Depends(get_current_user)):
    meeting = Meeting.objects(id=meeting_id).first()
    if not meeting:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meeting not found")
    if str(meeting.authorId) != str(current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    update_data = body.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(meeting, key, value)
    meeting.save()
    return _meeting_to_response(meeting)


@router.delete("/{meeting_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_meeting(meeting_id: str, current_user: User = Depends(get_current_user)):
    meeting = Meeting.objects(id=meeting_id).first()
    if not meeting:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meeting not found")
    if str(meeting.authorId) != str(current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    meeting.delete()
