from datetime import datetime, timezone
from math import ceil

from fastapi import APIRouter, Depends, HTTPException, Query, status

from dependencies import get_current_user, optional_current_user
from models.post import Post
from models.user import User
from schemas.common import PaginatedResponse
from schemas.post import PostCreate, PostResponse, PostUpdate

router = APIRouter(prefix="/api/posts", tags=["Posts"])


def _post_to_response(p: Post) -> PostResponse:
    return PostResponse(
        id=str(p.id),
        title=p.title,
        content=p.content,
        image=p.image,
        authorId=p.authorId,
        authorName=p.authorName,
        authorAvatar=p.authorAvatar,
        eventId=p.eventId,
        likes=p.likes,
        likedBy=p.likedBy or [],
        status=p.status,
        publishedAt=p.publishedAt.isoformat() if p.publishedAt else None,
        createdAt=p.createdAt.isoformat() if p.createdAt else "",
    )


@router.get("", response_model=PaginatedResponse)
def list_posts(
    _user: User | None = Depends(optional_current_user),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
):
    qs = Post.objects()
    if not _user:
        qs = qs.filter(status__ne="draft")
    total = qs.count()
    pages = ceil(total / limit) if total > 0 else 1
    items = [_post_to_response(p) for p in qs.order_by("-createdAt").skip(skip).limit(limit)]
    return PaginatedResponse(items=items, total=total, page=(skip // limit) + 1, pages=pages)


@router.post("", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
def create_post(body: PostCreate, current_user: User = Depends(get_current_user)):
    post = Post(
        title=body.title,
        content=body.content,
        image=body.image,
        eventId=body.eventId,
        status=body.status,
        authorId=str(current_user.id),
        authorName=current_user.username,
        authorAvatar=current_user.avatar,
        publishedAt=datetime.now(timezone.utc) if body.status == "published" else None,
    )
    post.save()
    return _post_to_response(post)


@router.get("/{post_id}", response_model=PostResponse)
def get_post(post_id: str, _user: User | None = Depends(optional_current_user)):
    post = Post.objects(id=post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return _post_to_response(post)


@router.patch("/{post_id}", response_model=PostResponse)
def update_post(post_id: str, body: PostUpdate, current_user: User = Depends(get_current_user)):
    post = Post.objects(id=post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    update_data = body.model_dump(exclude_unset=True)
    only_likes = set(update_data.keys()) == {"likes"}
    if str(post.authorId) != str(current_user.id) and not only_likes:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    if "likes" in update_data:
        user_id = str(current_user.id)
        if not post.likedBy:
            post.likedBy = []
        if user_id in post.likedBy:
            post.likedBy.remove(user_id)
        else:
            post.likedBy.append(user_id)
        post.likes = len(post.likedBy)
        del update_data["likes"]
    for key, value in update_data.items():
        setattr(post, key, value)
    if "status" in update_data and update_data["status"] == "published" and not post.publishedAt:
        post.publishedAt = datetime.now(timezone.utc)
    post.save()
    return _post_to_response(post)


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: str, current_user: User = Depends(get_current_user)):
    post = Post.objects(id=post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    if str(post.authorId) != str(current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    post.delete()
