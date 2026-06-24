from pydantic import BaseModel, EmailStr


class SignupRequest(BaseModel):
    username: str
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access: str


class UserProfileResponse(BaseModel):
    id: str
    name: str
    email: str
    role: str
    bio: str
    avatar: str


class UserProfileUpdate(BaseModel):
    name: str | None = None
    email: str | None = None
    role: str | None = None
    bio: str | None = None
    avatar: str | None = None


class PasswordUpdate(BaseModel):
    currentPassword: str
    newPassword: str
