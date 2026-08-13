from pydantic import BaseModel, Field


class JobResponse(BaseModel):
    id: int
    external_id: str
    title: str
    company: str
    location: str
    salary_min: int | None = None
    salary_max: int | None = None
    employment_type: str | None = None
    seniority_level: str | None = None
    posted_at: str
    fraud_score: int = 0

    class Config:
        from_attributes = True


class JobMatchScoreResponse(BaseModel):
    job_id: int
    overall_match: int = Field(ge=0, le=100)
    matched_skills: list[str]
    missing_skills: list[str]
    match_category: str = Field(default='Medium')  # High, Medium, Low
    explanation: str
