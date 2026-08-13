from pydantic import BaseModel, Field


class ProfileCreateRequest(BaseModel):
    location: str | None = None
    phone: str | None = None
    bio: str | None = None
    target_roles: list[str] | None = None
    preferred_locations: list[str] | None = None
    min_salary: int | None = None
    max_salary: int | None = None
    experience_level: str | None = None


class ProfileResponse(BaseModel):
    id: int
    user_id: int
    location: str | None
    phone: str | None
    profile_completeness: int = Field(default=0, ge=0, le=100)
    target_roles: list[str] | None = None
    experience_level: str | None = None

    class Config:
        from_attributes = True
