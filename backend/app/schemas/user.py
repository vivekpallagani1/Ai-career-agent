from pydantic import BaseModel, EmailStr, Field


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    name: str
    role: str = 'candidate'

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = 'bearer'
    user: UserResponse
