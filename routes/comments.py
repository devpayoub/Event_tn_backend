from fastapi import APIRouter, Depends, HTTPException, Query, status

from dependencies import get_current_user, optional_current_user
from models.comment import Comment
from models.user import User
from schemas.comment import CommentCreate, CommentResponse, CommentUpdate

router = APIRouter(prefix="/api/comments", tags=["Comments"])


def _comment_to_response(c: Comment) -> CommentResponse:
    return CommentResponse(
        id=str(c.id),
        postId=c.postId,
        eventId=c.eventId,
        parentId=c.parentId or None,
        authorId=c.authorId,
        authorName=c.authorName,
        authorAvatar=c.authorAvatar,
        content=c.content,
        timestamp=c.timestamp.isoformat() if c.timestamp else "",
    )


@router.get("", response_model=list[CommentResponse])
def list_comments(
    postId: str | None = Query(None),
    eventId: str | None = Query(None),
    _user: User | None = Depends(optional_current_user),
):
    if postId:
        comments = Comment.objects(postId=postId).order_by("timestamp")
    elif eventId:
        comments = Comment.objects(eventId=eventId).order_by("timestamp")
    else:
        comments = []
    return [_comment_to_response(c) for c in comments]


@router.post("", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
def create_comment(body: CommentCreate, current_user: User = Depends(get_current_user)):
    comment = Comment(
        postId=body.postId,
        eventId=body.eventId,
        parentId=body.parentId or "",
        authorId=str(current_user.id),
        authorName=current_user.username,
        authorAvatar=current_user.avatar,
        content=body.content,
    )
    comment.save()
    return _comment_to_response(comment)


@router.patch("/{comment_id}", response_model=CommentResponse)
def update_comment(comment_id: str, body: CommentUpdate, current_user: User = Depends(get_current_user)):
    comment = Comment.objects(id=comment_id).first()
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
    if comment.authorId != str(current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    if body.content is not None:
        comment.content = body.content
    comment.save()
    return _comment_to_response(comment)


@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(comment_id: str, current_user: User = Depends(get_current_user)):
    comment = Comment.objects(id=comment_id).first()
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
    if comment.authorId != str(current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    comment.delete()
