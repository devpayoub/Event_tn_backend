from fastapi import APIRouter, Depends, HTTPException, status

from auth import hash_password, verify_password
from dependencies import get_current_user
from models.user import User
from schemas.user import PasswordUpdate, UserProfileResponse, UserProfileUpdate

router = APIRouter(prefix="/api/user", tags=["Users"])


def _user_to_response(user: User) -> UserProfileResponse:
    return UserProfileResponse(
        id=str(user.id),
        name=user.username,
        email=user.email,
        role=user.role,
        bio=user.bio,
        avatar=user.avatar,
    )


@router.get("/profile", response_model=UserProfileResponse)
def get_profile(current_user: User = Depends(get_current_user)):
    return _user_to_response(current_user)


@router.patch("/profile", response_model=UserProfileResponse)
def update_profile(body: UserProfileUpdate, current_user: User = Depends(get_current_user)):
    if body.name is not None:
        current_user.username = body.name
    if body.email is not None:
        current_user.email = body.email
    if body.role is not None:
        current_user.role = body.role
    if body.bio is not None:
        current_user.bio = body.bio
    if body.avatar is not None:
        current_user.avatar = body.avatar
    current_user.save()
    return _user_to_response(current_user)


@router.patch("/password")
def update_password(body: PasswordUpdate, current_user: User = Depends(get_current_user)):
    if not verify_password(body.currentPassword, current_user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Current password is incorrect")
    current_user.password = hash_password(body.newPassword)
    current_user.save()
    return {"status": "ok"}
