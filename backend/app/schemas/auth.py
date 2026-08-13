from pydantic import BaseModel, EmailStr


class UserRegisterRequest(BaseModel):
    email: EmailStr
    password: str
    name: str


class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str
