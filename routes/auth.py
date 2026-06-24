from fastapi import APIRouter, HTTPException, status
from mongoengine.errors import NotUniqueError

from auth import create_access_token, hash_password, verify_password
from models.user import User
from schemas.user import LoginRequest, SignupRequest, TokenResponse, UserProfileResponse

router = APIRouter(prefix="/api/auth", tags=["Auth"])


@router.post("/signup", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def signup(body: SignupRequest):
    if User.objects(username=body.username).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken")
    if User.objects(email=body.email).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    user = User(
        username=body.username,
        email=body.email,
        password=hash_password(body.password),
    )
    try:
        user.save()
    except NotUniqueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
    token = create_access_token(str(user.id))
    return TokenResponse(access=token)


@router.post("/login", response_model=TokenResponse)
def login(body: LoginRequest):
    user = User.objects(email=body.email).first()
    if not user or not verify_password(body.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    token = create_access_token(str(user.id))
    return TokenResponse(access=token)
